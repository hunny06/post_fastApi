# def collidingAsteroids(asteroids):
    # 3,-2,4 = 3, 4

    # 6 7 -9 -9 7 = -9 7
    #  3 4 5 -2 7 = 3 4 5 7

    # for i in range(1,len(asteroids)-1):
        # if (asteroids[i] < 0):
            

    #     print(asteroids,i,)
    #     print(asteroids[i])
    #     if asteroids[i] < 0:
    #         current_ast = abs(asteroids[i])
    #         index = i
    #         if(current_ast == asteroids[index-1]):
    #             asteroids.remove(asteroids[i])
    #             asteroids.remove(asteroids[i-1])

    #         elif(current_ast < asteroids[index-1]):
    #             asteroids.remove(asteroids[index])

    #         while(current_ast > asteroids[index-1] ):
    #             asteroids.remove(asteroids[index-1])
    #             if index == 0:
    #                 break
    #             index-=1


    # return asteroids

# mat = [3, -6, -4, 1, 5, 7, 3, -6, 5, 6 ]
# result = collidingAsteroids(mat)
# print(result)

#Your code goes here

# length = int(input("Enter Length = "))
# breath = int(input("Enter Breath = "))

# area = length*breath
# print(area)
text = input().split()
print(text)
print(f"The name of the person is {text[0]} and the age is {text[1]}.")


