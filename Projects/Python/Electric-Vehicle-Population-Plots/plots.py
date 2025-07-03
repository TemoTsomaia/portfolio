import pandas as pd
import sqlite3
import threading
import matplotlib.pyplot as plt

class ElectricVehicleCharts:
    def __init__(self, csv_p):
        #Take path of .csv file and declare a path to database. top_brands and tesla_count are objects that are being populated that lately will be illustrated
        self.csv_p = csv_p
        self._db_p = 'electric_vehicles.db'
        self.top_brands = None
        self.tesla_count = None
        try:
            #Load the CSV file and clean its data
            self.data_csv = pd.read_csv(self.csv_p)
            self.__clean_data()

            #Threads
            t1 = threading.Thread(target=self.__get_top_brands)
            t2 = threading.Thread(target =self.__get_tesla_model_counts)

            t1.start()
            t2.start()

            t1.join()
            t2.join()

        #Catch exceptions while reading/cleaning data and trying to create threads that will populate top brands and tesla count attributes
        except Exception as e:
            print(f"We've encountered an error: {e}")


    def __get_top_brands(self, top_n=5):
        #Commented code can be used to do kind of do the same but using database itself
        #query = "SELECT Make FROM electric_vehicles"
        #df_from_db = pd.read_sql_query(query, connection)
        try:
            #processes the `Make` column in the dataset to determine "top_n" most frequently
            #occurring brands and stores the result in the `self.top_brands` attribute.
            self.top_brands = self.data_csv["Make"].value_counts().head(top_n)
        except Exception as e:
            return f"Couldn't get top brands: {e}"

    def __get_tesla_model_counts(self):
        try:
            # Filters the dataset (`self.data_csv`) to include only rows where the `Make` column (case-insensitively) matches "TESLA" and strips it.
            teslas = self.data_csv[self.data_csv["Make"].str.strip().str.upper() == "TESLA"]
            # Get the counts of each unique model
            self.tesla_count = teslas["Model"].value_counts()
        except Exception as e:
            return f"Couldn't process and get Tesla models counts: {e}"

    def __clean_data(self):
        def check_make(): #Method to check collumns "Make" if they consist of strings only
            self.data_csv["Make"] = self.data_csv["Make"].astype(str)

        def check_type(): #Method to check collumns "Electric Vehicle Type" if they consist of strings only
            self.data_csv["Electric Vehicle Type"] = self.data_csv["Electric Vehicle Type"].astype(str)

        def check_model(): #Method to check collumns "Model" if they consist of strings only
            self.data_csv["Model"] = self.data_csv["Model"].astype(str)

        try:
            # Delete rows with missing critical data
            self.data_csv = self.data_csv.dropna(subset=["Make", "Electric Vehicle Type", "Model"])

            #Threads
            t1 = threading.Thread(target=check_make)
            t2 = threading.Thread(target=check_type)
            t3 = threading.Thread(target=check_model)

            t1.start()
            t2.start()
            t3.start()

            t1.join()
            t2.join()
            t3.join()

        except Exception as e:
            print(f"Couldn't clean data or start Thread: {e}")



    def save_to_database(self):
        try:
            #Opens a connection to the SQLite database located at `self._db_p`, Writes the `self.data_csv` DataFrame to the table
            #If the table already exists, it is replaced with the new data.
            self.data_csv.to_sql("electric_vehicles", sqlite3.connect(self._db_p), if_exists="replace", index=False)
            print("Data saved to database successfully.")
            #Closes the database connection after writing.
            sqlite3.connect(self._db_p).close()
        except Exception as e:
            print(f"Couldn't save to database: {e}")


    def plot_top_brands(self, top_n = 5):
        try:
            #Plot the data
            plt.figure(figsize=(10, 6))
            colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF']
            self.top_brands.plot(kind='bar', color=colors)

            # Add title and labels
            plt.title(f"Top {top_n} Electric Vehicle Brands", fontsize=16)
            plt.xlabel("Brand", fontsize=14)
            plt.ylabel("Number of Vehicles", fontsize=14)

            # Show grid and plot
            plt.grid(axis='y', linestyle='--', alpha=0.7)  #horizontal grid lines with "--" style and 70% opacity
            plt.xticks(rotation=45, fontsize=12) #rotated labels
            plt.tight_layout() #Automatically adjusts the spacing between chart elements to ensure nothing overlaps.
            plt.show()
        except Exception as e:
            print(f"Couldn't plot top brands: {e}")


    def plot_tesla_model_counts(self):
        try:
            # Get Tesla model counts


            # Calculate percentages for the legend
            total = self.tesla_count.sum() #total amount of Teslas
            labels_with_percentages = [ #Use pandas series as key,value data structure to create labels for legend
                f"{model} ({count} - {count / total * 100:.2f}%)"
                for model, count in self.tesla_count.items()
            ]

            # Plot the pie chart
            plt.figure(figsize=(8,8))


            colors = ['#FF0000', '#FF4D4D', '#FF8080', '#FFB3B3', '#FFE5E5', '#FFF2F2'] #Colours fading away

            #Styling plot
            self.tesla_count.plot(
                kind='pie',
                startangle=140,
                colors=colors,
                legend=False,  # Disable the default legend
            )

            # Add a legend with names and percentages
            plt.legend(
                labels_with_percentages,
                title="Tesla Models (Count - %)",
                loc="upper right", #location
                bbox_to_anchor=(1.3, 1), #Size of the legend
                fontsize=10,
            )

            # Add title and adjust layout
            plt.title("Tesla Models Distribution by Percentage", fontsize=16)
            plt.ylabel("")  # Removes the default y-axis label
            plt.tight_layout() #Automatically adjusts the spacing between chart elements to ensure nothing overlaps.
            plt.show()
        except Exception as e:
            print(f"Couldn't plot Tesla models count: {e}")


def main():
    file = 'Electric_Vehicle_Population_Data.csv'
    data_with_charts = ElectricVehicleCharts(file)  #Create class under file directory "Electric_Vehicle_Population_Data.csv"
    data_with_charts.save_to_database() #Save read data into the database under predefined path 'electric_vehicles.db'


    data_with_charts.plot_top_brands()  #plot bar chart for top brands
    data_with_charts.plot_tesla_model_counts()  #plot pie chart for tesla models


if __name__ == "__main__":
    main()

