from apis import spotify
from apis import twilio
import random

user_selections = {
    'genres': [],
    'artists': []
}


def print_menu():
    print('''
---------------------------------------------------------------------
Settings / Browse Options
---------------------------------------------------------------------
1 - Select your favorite genres
2 - Select your favorite artists
3 - Discover new music
4 - Quit
---------------------------------------------------------------------
    ''')

artist_list = []
artist_id_list= []
list_genre = spotify.get_genres_abridged()
selected_genre_nums = []
selected_genres = []
artist_list_for_search = []
first_id_list = []
artist_id_list = []


def handle_genre_selection():
    
    print('Selecting genres')
    counter = 0
    for g in list_genre:
        print(counter, g)
        counter = counter + 1

     
    while True:
        check = True
        selected_genre_numbers = input('Select you genre(s) by number and separate selection with a comma or input clear to clear the list: ')
        selected_genre_nums = selected_genre_numbers.split(',')
    
        

        for value in selected_genre_nums:
            if value.isnumeric() == False: 
                check = False
        
        if selected_genre_numbers.lower() == 'clear':
            selected_genre_numbers = ''
            print('You cleared your selections.', selected_genres)
            selected_genres.clear()
            break

        elif check == False:
            print('Please try again using integer numbers and commas')
            selected_genre_numbers = ''
            selected_genre_numbs = ''
            continue
       
        else:
            selected_genre_nums = selected_genre_numbers.split(',')

            for genre_select in selected_genre_nums:
                if int(genre_select) > 24:
                    continue
                elif list_genre[int(genre_select)] in selected_genres:
                    continue
                else:
                    selected_genres.append(list_genre[int(genre_select)])
            break

    print('These are your selected genres:', selected_genres)       
        
    
    
    # 1. Allow user to select one or more genres using the
    #    spotify.get_genres_abridged() function
    # 2. Allow user to store / modify / retrieve genres
    #    in order to get song recommendations


def handle_artist_selection():
    check2 = True
    spotify_artists = []
    print('Selecting artists')
 
    first_artist = input('Provide one or more artist separated with commas or input clear to clear the artist list: ')
    first_artist_separated = first_artist.split(',')
       
    
    if first_artist.lower() == 'clear':
        artist_list.clear()
        artist_list_for_search.clear()
        print('You have cleared the artist list: ',artist_list)
        big_check = False
        return

    for artist_1 in first_artist_separated:
        spotify_artists = spotify_artists + spotify.get_artists(artist_1)

    counter2 = 0 
    for artist in spotify_artists:
        first_id_list.append(artist.get('id'))
        print(counter2, artist.get('name'))
        counter2 = counter2 + 1

    while check2 == True:
        check = True 
        number_selection_commas = input('Input the numbers of the artist(s) you would like to select separated by commas or input clear to clear the list: ')
        number_selection = number_selection_commas.split(',')

        for num_check in number_selection:
            if num_check.isnumeric() == False:
                check = False
        

        if check == False:
            print('Please try again using numbers and commas')
            number_selection.clear()
            continue
        else:
            check2 = False
                
    for num in number_selection:
        num_int = int(num)
        if num_int > counter2:
             continue
        else:
            artist_list_for_search.append(spotify_artists[num_int].get('name'))
                                  
     
    print('These are the artists spotify will search with:', artist_list_for_search)
    check2 = False
        





    

   

  # ask for artist, check, get dictionary or artist and related artist, first element of list is the artist we are looking for, 
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations


def get_recommendations():
    list_genre_rec = []
    list_artist_id_rec = []
    rec_list = []
    gcap = len(selected_genres)
    acap = len(artist_list_for_search)
    if gcap == 1:
        list_genre_rec.append(selected_genres[0])
    elif gcap > 1:
        list_genre_rec.append(selected_genres[random.randint(1,gcap-1)])
        list_genre_rec.append(selected_genres[0])
    else:
        list_genre_rec = list_genre_rec

    if acap == 1:
        list_artist_id_rec.append(first_id_list[0]) 
    elif acap == 2:
        list_artist_id_rec.append(first_id_list[1])
        list_artist_id_rec.append(first_id_list[0])
    elif acap > 2:
        list_artist_id_rec.append(first_id_list[random.randint(1,acap-2)])
        list_artist_id_rec.append(first_id_list[0])
        list_artist_id_rec.append(first_id_list[acap-1])
   
    
    rec_list = spotify.get_similar_tracks(artist_ids = list_artist_id_rec, genres = list_genre_rec)

    song_list = spotify.get_formatted_tracklist_table(rec_list)

    print(song_list)

    link = spotify.get_formatted_tracklist_table_html(rec_list)
    


    x = True

    while x == True:
        email_send = input('would you like to email the tracklist send? YES or NO: ')
        if email_send == 'YES':
            account = input('What is your email address? ')
            receiver = input('Who would you like to send the tracklist to? ')
            subject = input('What do you want the subject line to say? ')
            twilio.send_mail(account, receiver, subject, link)
            x = False

        elif email_send == 'NO':
            None
            x = False

        else:
            print('Invalid answer')
            continue
 
      
    
    #print('Handle retrieving a list of recommendations here...')
    # 1. Allow user to retrieve song recommendations using the
    #    spotify.get_similar_tracks() function
    # 2. List them below


# Begin Main Program Loop:
while True:
    print_menu()
    choice = input('What would you like to do? ')
    if choice == '1':
        handle_genre_selection()
    elif choice == '2':
        handle_artist_selection()
    elif choice == '3':
        get_recommendations()
        
        # In addition to showing the user recommendations, allow them
        # to email recommendations to one or more of their friends using
        # the twilio.send_mail() function.

    elif choice == '4':
        print('Quitting...')
        break
    else:
        print(choice, 'is an invalid choice. Please try again.')
    print()
    input('Press enter to continue...')
