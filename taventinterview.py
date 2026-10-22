# second larget number in a list 

numbers = [20, 40 , 30]

max = 0

def secondLargest(data : list):
        if len(data) > 0:
                data.sort()
                return data[1]
             
print(secondLargest(numbers)) 
     
    
    

