list1 = [1, 2, 3, 3, 6, 12] 
list2 = [5, 6, 7, 5] 
list3 = [10, 11, 12]
  
# Lists converted to sets 
set1 = set(list2) 
set2 = set(list1)
print(set1)
  
# Update method 
set1.update(list1)
   
# Print the updated set 
print(set1) 
  
  
# List is passed as an parameter which 
# gets automatically converted to a set 
set1.update(list3) 
print(set1)