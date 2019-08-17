#!/usr/bin/python

from datetime import date, datetime, timedelta
from calendar import Feature_Date
import time
import operator

class Feature_Accounts:
    def __init__(self):
        self.user_accounts = [] #Savings, Checkings, etc...
        self.incomes = []		#:Monthly paycheck, selling stock, etc...
        self.deductions = []	#Rent, CellPhone bill, etc...
        self.save_for = []
        self.user = Feature_Date()
        self.hasBeenLoaded = False

    #returns the account dict for def /getAccounts in app.py
    def return_user_accounts(self):
        return self.user_accounts

    #Returns the income dict for def /getIncomes in app.py
    def return_user_incomes(self):
        return self.incomes

    #Returns the income dict for def /getDeductions in app.py
    def return_user_deductions(self):
        return self.deductions

    #returns the account dic for def /showAccounts in app.py
    def return_account_dic(self):
        return self.user_accounts

    #return save_for
    def return_save_for(self):
        return self.save_for

    #Adds a account to the user
    def add_account(self, account_name, amount_saved):
    	self.user_accounts.append({'account': account_name,
    				               'saved': amount_saved})

    #Adds incomes to the user
    def add_income(self, _paid, _job, _frequency, _payday, d_account):
    	#_payday = self.user.translate_to_date(payday)
    	self.incomes.append({'paid': 			_paid,
    			             'ttype': 			_job,
    			             'frequency': 		_frequency,
    			             'payday': 			_payday,
    			             'deposit_account': d_account})

    #Adds deductions to the user
    def add_deduction(self, _amount, _type, _frequency, _date, d_account):
    	#date_ = self.user.translate_to_date(_date)
    	self.deductions.append({'amount':          _amount,
    				            'type':            _type,
    				            'frequency':       _frequency,
    			                'date':            _date,
    				            'deduct_account':  d_account})

    #Adds save for to the user
    def add_save_for(self, _desire, _date, _cost, d_account, start_date):
    	#date_ = self.user.translate_to_date(_date)
    	self.save_for.append({'desire':          _desire,
    				          'cost':            _cost,
    			              'date':            _date,
    				          'deduct_account':  d_account,
                              'start_date':      start_date})

    #Checks if any incomes are available today()
    def check_incomes(self):
        for income in self.incomes:
            if self.user.days_to_date(income.get('payday')) == 0:
    	        #print("Processing Payday.....")
        		#print("======================")
                search = [i for i, x in enumerate(self.user_accounts) if x['account'] == income.get('deposit_account')][0]
                income_amount = float(income.get('paid'))
            	account_sum = float(self.user_accounts[search].get('saved'))
            	account_sum += income_amount
            	self.user_accounts[search].update({'saved': account_sum})
            	#print("Account: " + str(self.user_accounts[search].get('account')))
            	#print("Total: " + str(self.user_accounts[search].get('saved')))

    #Checks if any deductions are available today() rip
    #function broken worked with console not with db

    def check_deductions(self):
        pass
    """
    	for deduction in self.deductions:
    	    if self.user.days_to_date(deduction.get('date')) == 0:
    	        print("Processing deduction")
        		search = [i for i, x in enumerate(self.user_accounts) if x['account'] == deduction.get('deduct_account')][0]
        		deduct_amount = float(deduction.get('amount'))
        		account_sum = float(self.user_accounts[search].get('saved'))
        		#may need to add feature later for what happens if deduction makes account goe below zero
        		account_sum -= deduct_amount
        		self.user_accounts[search].update({'saved': account_sum})
    """
    #Only deducts a specific expense
    def deduct_expense(self, _cost, _account):
        search = [i for i, in enumerate(self.user_accounts) if x['account'] == _account][0]
    	account_sum = float(self.user_accounts[search].get('saved'))
        account_sum -= _cost
        self.user_accounts[search].update({'saved': account_sum})

        #handles expenses user spends money from their account
    def deduct_all_expenses(self, user_object):
    	for expense in user_object.container:
    	    if expense.get('processed') == False:
    	        search = [i for i, x in enumerate(self.user_accounts) if x['account'] == expense.get('account')][0]
                exp_amount = float(expense.get('cost'))
            	account_sum = float(self.user_accounts[search].get('saved'))
            	account_sum -= exp_amount
            	self.user_accounts[search].update({'saved': account_sum})
            	expense.update({'processed': True})

    #Didnt work this feature adds save for stuff 
    #Added last minute. Does funcitonality to determine wether saving for an item by a date is reasonable to user
    def save_for_reasonability(self, sf, user_obj):
        span_sums = []
        weekly_avg, span_sums = user_obj.get_avg_spendings("week")
        end_date = user_obj.translate_to_date(sf.get('date'))
        start_date = user_obj.translate_to_date(sf.get('start_date'))
        incomeSum = deductionSum = avgSum = 0
        print("Did invoke?4")
        #could later migrate these two below for loops to a function with obj parameter
        #originally set up with while loop flask didnt like it and wanted concurrency
        for income in self.incomes:
            check_date = user_obj.translate_to_date(income.get('payday'))
            start_index = end_index = 0
            freq = int(income.get('frequency'))
            start_indexBool = True


            for i in range(20):
                freqMultiplied = i * freq

                if user_obj.is_date_between_dates(check_date, sf.get('start_date'), sf.get('date')) == True:
                    if start_indexBool == True:
                        start_index = i
                        start_indexBool = False
                    tempDate = check_date + timedelta(days=freqMultiplied)
                    if user_obj.is_date_between_dates(tempDate, sf.get('start_date'), sf.get('date')) == True:
                        end_index = i

                check_date = check_date + timedelta(days=freqMultiplied)

            occurences = end_index - start_index
            print("occurences: " + str(occurences))

            if occurences >= 1:
                incomeSum += float(income.get('paid')) * occurences
            else:
                incomeSum += 0

        print("Did invoke DEDUCTIONS=============")
        for deduction in self.deductions:
            check_date = user_obj.translate_to_date(deduction.get('date'))
            start_index = end_index = 0
            freq = int(deduction.get('frequency'))
            start_indexBool = True
            for i in range(20):
                freqMultiplied = i * freq
                if user_obj.is_date_between_dates(check_date, sf.get('start_date'), sf.get('date')) == True:
                    if start_indexBool == True:
                        start_index = i
                        start_indexBool = False
                    tempDate = check_date + timedelta(days=freqMultiplied)
                    if user_obj.is_date_between_dates(tempDate, sf.get('start_date'), sf.get('date')) == True:
                        end_index = i
                check_date = check_date + timedelta(days=freqMultiplied)
            occurences = end_index - start_index

            if occurences >= 1:
                deductionSum += float(deduction.get('paid')) * occurences
            else:
                deductionSum += 0
        print("Did invoke?4123213123")
        end_index = 0
        freq = 7
        check_date = user_obj.translate_to_date(sf.get('date'))
        for i in range(50):
            freqMultiplied = i * freq
            if user_obj.is_date_between_dates(check_date, sf.get('start_date'), sf.get('date')) == True:
                newDate = start_date + timedelta(days=freqMultiplied)
                if user_obj_is_date_between_dates(newDate, start_date, end_date) == True:
                    end_index = i

        avgSum = end_index * weekly_avg

        print("Did invoke?4")
        total = (avgSum + incomeSum) - deductionSum
        if total >= 0:
            print("Tot Pos: " + str(total))
            return "Net Positive", total
        elif total < 0:
            print("Tot Neg: " + str(total))
            return "Net Negative", total



    #This function will give the user a choice to specifiy a percentage of money
    #to go into a select account
    #def paycheck_accounting(self):
    #	pass

    #Adds accounts from a txt files parsed data
    def from_parser_to_container(self, _storage):
        for data in _storage:
            self.add_account(data.get('account'), float(data.get('saved')))

        #prints the accounts available to user
    def print_accounts(self):
        for account in self.user_accounts:
    	    name = account.get('account')
    	    save = account.get('saved')
    	    print("Account: " + str(name))
    	    print("Saved: " + str(save))


    #prints incomes available to user
    def print_incomes(self):
        for income in self.incomes:
            paid = income.get('paid')
            typed = income.get('ttype')
            freq = income.get('freq')
            payeday = income.get('payday')
            daccount = income.get('deposit_account')

            print("======================DATA=========================")
            print("Paid: " + str(paid) + "type: " + str(typed) + "freq: " + str(freq) + "date: " + str(payeday) + "Account: " + str(daccount))
