'''
Programming Assignment 1: non-personalized recommendations
Rita Cheng
'''

# constants
OUTPUT_COUNT = 5
MOVIE_LIST = [602,581,85]

# simple: set(uid), set(uid) -> int
# calculates the association formula (x and y) / x
def simple(x_reviewers, y_reviewers, **kwargs):
	both = x_reviewers.intersection(y_reviewers)
	both_count = float(len(both))

	return both_count / float(len(x_reviewers))
'''
tests
print simple({1,2,3}, {2,4,5}) # should be 1/3
print simple({1,2,3}, {4,5,6}) # should be 0
print simple({1,2,3}, {1,2,3}) # should be 1
'''

# advanced: set(uid), set(uid) -> int
# calculates the association formula ((x and y) / x) / ((!x and y) / !x)
def advanced(x_reviewers, y_reviewers, **kwargs):
	simple_count = simple(x_reviewers, y_reviewers)

	not_x_y = float(len(y_reviewers.difference(x_reviewers)))
	not_x = float(kwargs['total'] - len(x_reviewers))
	if not_x_y == 0 or not_x == 0: # prevent division by zero
		return 1
	return simple_count / (not_x_y / not_x)

'''
tests
print advanced({1,2,3}, {2,4,5}, total = 5) # should be (1/3)/(2/2)= 1/3
print advanced({1,2,3}, {4,5,6}, total = 6) # should be 0/(3/3) = 0
print advanced({1,2,3}, {1,2,3}, total = 3) # should be 1
'''

# calculate_closest_movies: dict(movies->users) function movie-id count -> list(movie id)
# outputs count sorted closest movies to movie-id according to the function
def calculate_closest_movies(movies, function, id, count, **kwargs):
	scores = []
	x_reviewers = movies[id]
	for y,y_reviewers in movies.iteritems():
		if id==y:
			continue

		scores.append((y, function(x_reviewers, y_reviewers, **kwargs)))
	scores.sort(key=lambda tup: tup[1], reverse=True) # sort by score

	return scores[:count]

# movie_formatting: list(list(int, float)) -> print int, float
# that wasn't clear

def movie_formatting(movies):
	output = "%s,%.2f" % (movies[0][0], movies[0][1]) #get first movie comma less

	for k, v in movies[1:]:
		output = "%s,%s" % (output, "%s,%.2f" % (k, v))
	
	return output

# print_closest_movies: dict(movies->users) list(movie-id) -> print(movie-ids)
# Print OUTPUT_COUNT closest movies with both simple and advanced formulas for each of the ids in ids
# output is formatted x-id, y-id-1, score-1, y-id-2, y-id-3, etc.
def print_closest_movies(movies, ids, **kwargs):
	print "Simple Formula"
	f = open('simple.txt', 'w')
	for id in ids:
		closest_movies = movie_formatting(calculate_closest_movies(movies, simple, id, OUTPUT_COUNT))
		print "%s,%s" %(id, closest_movies)
		f.write("%s,%s\n" %(id, closest_movies))
	f.close()
	
	print "Advanced Formula"
	f = open('advanced.txt', 'w')
	for id in ids:
		closest_movies = movie_formatting(calculate_closest_movies(movies, advanced, id, OUTPUT_COUNT, **kwargs))
		print "%s,%s" %(id, closest_movies)
		f.write("%s,%s\n" %(id, closest_movies))
	f.close()

# main
# process csv file, outputs dictionary of movies and users, and a list of users
def main():
    movies = {}
    reviewers = set()
    with open("recsys-data-ratings.csv") as fobj: # assume each line is formatting as userid, movieid, rating
        for line in fobj:
            uid, mid, rating = line.split(',')
            uid, mid = int(uid), int(mid)
            reviewers.add(uid)
            
            if not movies.has_key(mid):
            	movies[mid] = set()

            movies[mid].add(uid)
    
    total_reviewers = len(reviewers)
    print_closest_movies(movies, MOVIE_LIST, total = total_reviewers)

  

if __name__ == "__main__":
    main()