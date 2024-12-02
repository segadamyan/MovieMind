from datasource import MovieDatasource


if __name__ == "__main__":
    datasource = MovieDatasource(api_key="9f16f7879fbfa3a63037be63e224464a")
    datasource.update_movies(pages=1)
    # datasource.index_wrapper.save_index()
    # datasource.index_wrapper.load_index()
    query = "The untold origin story of Optimus Prime and Megatron, better known as sworn enemies, but once were friends bonded like brothers who changed the fate of Cybertron forever."

  
    results = datasource.search_movie(query)

    for result in results:
        print(f"Movie ID: {result['movie_id']}, Title: {result['title']}, Overview: {result['overview']}, Distance: {result['distance']}")