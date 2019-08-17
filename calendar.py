#!/usr/bin/python
"""Program Structure (running into naming things similarily
    _var is a function parameter
    var_ is a local variable
"""
#imports
from datetime import date, datetime, timedelta
import time
import operator
from decimal import Decimal, ROUND_UP

class Feature_Date:
    """
    ============================CONSTRUCTOR============================
    """
    def __init__(self):
        self.container = [] #Dictionary that contains {date, category, cost}
        self.categories = [] #Keeps a list of all of the different categories seen

    """
    =======================MAIN ROUTINE FUNCTIONS=======================
    """
    #Adds expenses to a list may later use a data structure date is yyyymmdd keeps track of new categories
    def add_expense(self, _cost, _category, _date, _account):
        date_ = self.translate_to_date(_date)
        self.container.append({'date':      date_,
                               'category':  _category,
                               'cost':      _cost,
                               'account':   _account,
                               'processed': False})

        if self.is_new_category(_category) == True:
            self.categories.append(_category)

    #This function returns avg weekly or monthly spending from a given list
    def get_avg_spendings(self, span):
        span_sums = []
        span_avg = 0
        start = end = span_counter = 0
        i = 0
        for items in self.container:
            if i == 0:
                span_sums.append(items.get('cost'))
            else:
                if self.is_date_between_dates(items.get('date'), start, end) == True:
                    span_sums[span_counter] += items.get('cost')
                else:
                    span_counter += 1
                    span_sums.append(items.get('cost'))

            span_avg += float(items.get('cost'))
            start, end = self.get_start_end_for_avg(span, items.get('date'))
            i += 1
        print("Calculating avg....")
        for s_sum in span_sums:
            print("Span Sum: $" + str(s_sum))

        avg = float(span_avg / (span_counter + 1))
        return avg, span_sums

    #Returns the avgerage spending per item in category: span will be, monthly, weekly, all(for all time and eternity muahahhaha)
    #UPDATE: 8/13/19
    #Added it to return the sum for all items spent to create a percentage for pie chart
    def get_avg_category_spendings(self, span):
        category_sums = [0]*len(self.categories)
        category_counts = [0]*len(self.categories)
        avgs = []
        #start = _start _start is a parameter maybe this is where i set options

        for i in range(len(self.container)):
            index = self.categories.index(self.container[i].get('category'))
            if span == "all":
                category_sums[index] += self.container[i].get('cost')
                category_counts[index] += 1
            else:
                start, end = self.get_start_end_for_avg(span, self.container[i].get('date'))
        #Original version returned an array of just the averages in order. Now it will return
        #a json for the pie chart and or line plot
        sum = 0

        for i in range(len(category_sums)):
            avgs.append({
                'Category': self.categories[i],
                'Average': float(category_sums[i] / category_counts[i])
            })

        return avgs, category_sums

    def get_total_spent_month(self, _dt):
        dt_ = self.translate_to_date(_dt)

        m_sum = 0
        start, end = self.get_start_end_for_avg("month", dt_)
        for items in self.container:
            if self.is_date_between_dates(items.get('date'), start, end) == True:
                m_sum += float(items.get('cost'))

        return m_sum

    #functionality for monthly expenses
    def expense_statistics(self):
        self.container = sorted(self.container, key = operator.itemgetter('date'))
        category_avg = []
        category_sums = []
        pie_dict = []
        #print("Printing Expense Statistics...")
        #print("==============================")
        #allWeekly = self.get_avg_weekly_spendings()
        #allMonthly = self.get_avg_monthly_spendings()
        #print("DOES IT GET HERE??????")
        category_avg, category_sums = self.get_avg_category_spendings("all")
        pie_dict = self.create_pie_chart_data(category_avg, category_sums)


        return category_avg, pie_dict
        #self.print_category_avgs(category_avg)
        #temp = self.get_total_spent_month("20190605")
        #category, span, start, end = self.filter_selection_handler()
        #self.apply_filter(category, span, start, end)

        #print("Average weekly spending: $" + str(weekly))
        #print("Average monthly spending: $" + str(monthly))
        #print("Month of June: $" + str(temp))
        #self.print_per_weekly_category()
        #self.print_per_monthly_category()

    """
    =======================ROUTINE HELPER FUNCTIONS=======================
    """
    #This function turns yyyymmdd to the datetime format yyyy-mm-dd
    def translate_to_date(self, _date):
        yyyy = int(_date[0:4])
        mm = int(_date[4:6])
        dd = int(_date[6:8])
        to_date = date(yyyy, mm, dd)
        return to_date

    #This function takes data read from a file stores and stores them
    def from_parser_to_container(self, _storage):
        for data in _storage:
            self.add_expense(float(data.get('cost')), data.get('category'), data.get('date'), data.get('account'))

    #checks if a item is in the list of categories seen
    def is_new_category(self, _category):
        if _category in self.categories:
            return False

        return True

    #returns start end date for the week of the date supplied
    def get_week_start_end(self, dt):
        start = dt - timedelta(days = dt.weekday())
        end = start + timedelta(days=6)
        return start, end

    #gets first day of a month of a given date
    def get_month_first_day(self, dt, d_years = 0, d_months = 0):
        y, m = dt.year + d_years, dt.month + d_months
        a, m = divmod(m-1, 12)
        return date(y+a, m+1, 1)

    #gets last day of a month of a given date
    def get_month_last_day(self, dt):
        return self.get_month_first_day(dt, 0, 1) + timedelta(-1)

    #returns start and end dates for get_avg_spendings function
    def get_start_end_for_avg(self, span, dt):
        if span == "week":
            return self.get_week_start_end(dt)
        elif span == "month": #if span == month
            return self.get_month_first_day(dt), self.get_month_last_day(dt)

    #returns avg weekly spending
    def get_avg_weekly_spendings(self):
        return self.get_avg_spendings("week")

    #This function returns avg monthly spendings
    def get_avg_monthly_spendings(self):
        return self.get_avg_spendings("month")

    #Returns T/F if boolean is between two dates
    def is_date_between_dates(self, _date, _from, _to):
        if (_date - _from).days >= 0 and (_date - _to).days <= 0:
            return True
        else:
            return False

    #Gets total spent between two dates
    def total_spent_between_dates(self, _from, _to):
        total = 0
        for pages in self.container:
            if(self.is_date_between_dates(pages.get('date'), _from, _to) == True):
                total += pages.get('cost')

        return total

    #Returns the number of days until a date occurs from todays date to_date is in yyyymmdd
    def days_to_date(self, to_date):
        today = date.today()
        set_date = self.translate_to_date(to_date)
        days = abs(set_date - today).days
        return days

    def days_to_date_from_date(self, to_date, from_date):
        f_date = self.translate_to_date(from_date)
        set_date = self.translate_to_date(to_date)
        days = abs(set_date - f_date).days
        return days

    def create_pie_chart_data(self, _data, _sums):
        pie_dict = []
        sum = 0
        for i in range(len(_sums)):
            sum += _sums[i]

        i = 0
        for data in _data:
            avg = _sums[i] / sum
            pie_dict.append({
                'Category': str(data.get('Category')),
                'Average':  str(Decimal(avg*100).quantize(Decimal(".1"), rounding=ROUND_UP))
            })
            i+=1
            print("Average: " + str(Decimal(avg*100).quantize(Decimal(".1"), rounding=ROUND_UP)))

        return pie_dict

    """
    ========================FLASK HELPER FUNCTIONS========================
    """
    #returns the dictionary of expenses
    def return_user_expenses(self):
        return self.container

    """
    =======================DEBUG PRINTING FUNCTIONS=======================
    """
    #prints object
    def print_object(self, _obj):
        print("Printing obj")
        for objects in _obj:
            print(str(objects))


    #prints the list of expenses also a name would be print_monthly_expenses()
    def print_expenses(self):
        print("Printing List....")
        print("=================")
        for pages in self.container:
            print("Cost: " + str(pages.get('cost'))),
            print("Category: " + str(pages.get('category'))),
            print("Date: " + str(pages.get('date'))),
            print("Visited: " + str(pages.get('processed')))
            print('\n')

    #helper function to print dates in list
    def print_dates(self):
        print("Printing list of dates...")
        print("=========================")
        for date_ in self.container:
            print(str(date_.get('date')))

        print('\n')

    #Helper function to print categories
    def print_categories(self):
        print("Printing Categories....")
        print("=======================")
        for item in self.categories:
            print(str(item))

    #Helper function to print categories with avgs
    def print_category_avgs(self, _category_avg):
        print("Printing Avgs.......")
        print("====================")
        for i in range(len(_category_avg)):
            print(self.categories[i] + ": " + str(_category_avg[i]))
        print('\n')


#END OF CLASS
