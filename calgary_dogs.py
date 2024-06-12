# calgary_dogs.py
# ABHIJITH DAVID
#
# A terminal-based application for computing and printing statistics based on given input.
# The main function loads the data from an Excel file, prompts the user to input a 
# dog breed, and checks if the breed exists in the dataset. 
# It then filters the data for the specified breed and provides Yearly data, total registration, yearly percentage & popular months.
import pandas as pd
import numpy as np

class DogBreed:
    """
    A class to analyze dog breed registration data in Calgary.
    """

    def __init__(self, calgary_dogs):
        """
        Initialize with the DataFrame containing dog registration data.

        Parameters:
        calgary_dogs : DataFrame containing dog registration data
            
        """
        self.calgary_dogs = calgary_dogs
        self.breed_input = ""
        self.breed_data = pd.DataFrame()

def main():
    """
    The main function to load data, process user input, and analyze dog breed registrations.
    """
    # Load data from Excel file
    calgary_dogs = pd.read_excel("CalgaryDogBreeds.xlsx")

    # Display the message
    print("ENSF 692 Dogs of Calgary")

    # Prompt user to input a dog breed
    breed_input = input("Enter a Dog Breed: ").strip().lower()

    # Check if the input breed exists in the data
    while breed_input not in calgary_dogs['Breed'].str.lower().unique():
        print("Dog breed not found in the data. Please try again.")
        breed_input = input("Enter a Dog Breed: ").strip().lower()

    # Confirm the selected breed
    print(f"You have selected: {breed_input.capitalize()}")

    # Create a multi-index DataFrame with Year and Month as the index
    calgary_dogs.set_index(['Year', 'Month'], inplace=True)

    # Use IndexSlice to select data for the breed
    idx = pd.IndexSlice
    breed_data = calgary_dogs.loc[idx[:, :], :]
    breed_data = breed_data[breed_data['Breed'].str.lower() == breed_input]

    # Get the list of years in the data
    years_listed = breed_data.index.get_level_values('Year').unique()
    print(f"The selected breed was listed in the following years: {', '.join(map(str, years_listed))}")

    # Calculate and display total registrations for the breed
    total_registrations = breed_data['Total'].sum()
    print(f"Total number of registrations for {breed_input.capitalize()}: {total_registrations}")

    # Calculate and print percentages of registrations for each year
    for year in years_listed:
        year_data = calgary_dogs.loc[idx[year, :], :]
        breed_year_total = breed_data.loc[idx[year, :], 'Total'].sum()
        year_total = year_data['Total'].sum()
        if year_total > 0:
            percentage = (breed_year_total / year_total) * 100
            print(f"Percentage of registrations in {year}: {percentage:.2f}%")
        else:
            print(f"No data for year {year}.")

    # Calculate and display the overall percentage of registrations
    total_breed_registrations = breed_data['Total'].sum()
    total_registrations_all_years = calgary_dogs['Total'].sum()
    overall_percentage = (total_breed_registrations / total_registrations_all_years) * 100
    print(f"Percentage of registrations over all years: {overall_percentage:.2f}%")

    # Masking operation to find most popular months for the breed's registrations
    max_registrations = breed_data['Total'].max()
    popular_months = breed_data[breed_data['Total'] == max_registrations].index.get_level_values('Month').unique()
    print(f"Most popular months for {breed_input.capitalize()} registrations: {', '.join(popular_months)}")


if __name__ == '__main__':
    main()

