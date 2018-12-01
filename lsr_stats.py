from statistics import mean #Import statistics module to calculate mean


#Recursive version
# def s_ab_rec(a_values, b_values, lastindex):
# 	if lastindex < 0: #Return zero when there is no more item to be recursed
# 		return 0
# 	else:
# 		a = (a_values[lastindex]-mean(a_values))#Calculate the difference between a and its mean
# 		b = (b_values[lastindex]-mean(b_values))#Calculate the difference between b and its mean
# 		return (a*b+s_ab_rec(a_values, b_values, lastindex-1)) #Return the sum of the product of these differences

def s_ab(a_values, b_values): #Assumes the length of the two lists are equal
	n = len(a_values)
	#Initialse each variable
	sumA, sumB, sumAB = 0, 0, 0
	for i in range(n):
		a, b = a_values[i], b_values[i]
		sumA += a
		sumB += b
		sumAB += a*b
	return (sumAB - (sumA * sumB)/n) #Calculate sums of squares and products (alternative formula)

def lse_b(x_values, y_values):#Calculate the b value of the regression line according to the formula
	return s_ab(x_values,y_values)/s_ab(x_values,x_values)

def lse_a(x_values, y_values): #Calculate the a value of the regression line according to the formula
	return mean(y_values) - mean(x_values)*lse_b(x_values,y_values)

