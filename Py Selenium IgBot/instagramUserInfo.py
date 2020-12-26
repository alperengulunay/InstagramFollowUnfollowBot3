"""
gets username, password and copy username
"""

class UserInfo:
    PATH = ""

    def getCopy(self , user , password):
        self.user_to_be_use = user + ".txt"
        self.username = user
        self.password = password
        self.random_copy_user = ""
        print("next account:" , self.user_to_be_use)
        
        file1 = open(f"{self.PATH}\\{user}\\{self.user_to_be_use}" , "r+")
        list1 = file1.readlines()
        """
        The algorithm that calculates the order in which the account names stored in the files will be retrieved
        """
        num1 = 0
        esitlik_count = 0
        ranking_number = 0
        
        try:
            for i in range(0,len(list1)):
                num = int(str(list1[i]).split(",")[1])
                if num == 0:
                    self.random_copy_user = str(list1[i]).split(",")[0]
                    ranking_number = i
                    break
                elif num < num1:
                    self.random_copy_user = str(list1[i]).split(",")[0]
                    ranking_number = i
                    break
                else:
                    num1 = num
                    esitlik_count +=1

            if esitlik_count == len(list1):
                self.random_copy_user = str(list1[0]).split(",")[0]
                ranking_number = 0
        finally:
            file1.close()

        a_file = open(f"{self.PATH}\\{user}\\{self.user_to_be_use}", "r+")
        lines = a_file.readlines()
        a_file.close()

        lines[ranking_number] = self.random_copy_user + "," + str(num + 1) + "\n"
        new_file = open(f"{self.PATH}\\{user}\\{self.user_to_be_use}", "w+")
        new_file.writelines(lines)
        new_file.close()