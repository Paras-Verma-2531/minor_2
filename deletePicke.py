import pickle

def empty_pickle_file(pickle_file):
    # Create an empty dictionary or appropriate data structure
    empty_data = {}

    # Write the empty data to the pickle file
    with open(pickle_file, 'wb') as f:
        pickle.dump(empty_data, f)

    print("Pickle file emptied successfully.")

# Example usage
pickle_file = './media/database/database_1.pickle'  # Your pickle file path

empty_pickle_file(pickle_file)
