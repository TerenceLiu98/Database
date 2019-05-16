from faker import Faker

fake = Faker(locale = 'en_US') 
N = int(input('how many data do you want:'))

for i in range(N):
    
    def name():
        return fake.name()
    def password():
        return fake.phone_number()  

if __name__=='__main__':
    print("NO:", i)
    print("name", name())
    print("password", password())


