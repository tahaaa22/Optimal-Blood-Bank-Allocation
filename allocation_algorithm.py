from models import Request, Hospital  
    
"""
TODO Rework the allocation algorithm to be compatible with the received requests
1. Allocate function receives an instance of the App Manager which in turn contains:
    - A list of hospitals (self.HOSPITALS)
    - A list of blood banks (self.BLOOD_BANKS)
    - Invenotry (self.INVENTORY)
    - A list of requests

2. The algorithm should prioritize the requests which consist of the following:
    - Hospital (request.hospital)
    - Requested blood type (request.blood_type)
    - Requested number of bags (request.number_of_blood_bags)
    - Remaining number of bags for that hospital (request.remaining_blood_bags)

3. The algorithm is expected to sort the requests list
"""
def allocate(app):
    score = {} # Dictionary to store the score of each hospital
    
    for request in app.requests: # O(n) complexity
        beds = request.hospital.number_of_beds
        requestTime =request.hours*60 + request.minutes 
        remaningBags = request.remaining_blood_bags
        score[request.id] = int(10 * requestTime + 7 * (1 / remaningBags) + 3 * beds)
        print(request, score[request.id])
    
    sorted_requests = sorted(app.requests, key=lambda h: score[h.id], reverse=True) # O(nlogn) complexity
    for request in sorted_requests:
        print(request)
    return sorted_requests