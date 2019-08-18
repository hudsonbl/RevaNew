from flask import Flask, render_template, request, json, session, redirect, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

#RevaNew py imports
from calendar import Feature_Date as fd
from Accounts import Feature_Accounts as fa
from datetime import date, datetime, timedelta
import operator

mysql = MySQL()
app = Flask(__name__)

app.secret_key = 'secret key'

#MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'conveyor'
app.config['MYSQL_DATABASE_PASSWORD'] = '77a7da320280a6a6379be231'
app.config['MYSQL_DATABASE_DB'] = 'RevaNew'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

##Global for gamestate of web app
userAccount = fa()
userLedger = fd()

"""
============================SESSION============================
"""
@app.route("/")
def main():
    return render_template('index.html')


@app.route("/userHome")
def userHome():
    try:
        if session.get('user'):

            _user = session.get('user')




            conn = mysql.connect()
            loadAccounts = conn.cursor()
            loadIncomes = conn.cursor()
            loadDeductions = conn.cursor()
            loadExpenses = conn.cursor()
            loadSF = conn.cursor()

            loadAccounts.callproc('sp_getAccountByUser', (_user,))
            accountData = loadAccounts.fetchall()

            loadIncomes.callproc('sp_getIncomeByUser', (_user,))
            incomeData = loadIncomes.fetchall()

            loadDeductions.callproc('sp_getDeductionByUser', (_user,))
            deductionData = loadDeductions.fetchall()

            loadExpenses.callproc('sp_getExpenseByUser', (_user,))
            expenseData = loadExpenses.fetchall()

            loadSF.callproc('sp_getSFByUser', (_user,))
            sfData = loadSF.fetchall()

            if not userAccount.return_user_accounts():
                for accounts in accountData:
                    userAccount.add_account(accounts[2], accounts[3])

            if not userAccount.return_user_incomes():
                for incomes in incomeData:
                    userAccount.add_income(incomes[3], incomes[2], incomes[5], incomes[4], incomes[6])

            if not userAccount.return_user_deductions():
                for deductions in deductionData:
                    userAccount.add_deduction(deductions[3], deductions[2], deductions[1], deductions[5], deductions[6])

            if not userLedger.return_user_expenses():
                for expenses in expenseData:
                    userLedger.add_expense(expenses[2], expenses[1], expenses[5], expenses[3])

            if not userAccount.return_save_for():
                for sf in sfData:
                    userAccount.add_save_for(sf[2], sf[1], sf[3], sf[5], sf[6])

            return render_template('userHome.html')
        else:
            return render_template('error.html')
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        loadAccounts.close()
        loadIncomes.close()
        loadDeductions.close()
        loadExpenses.close()
        loadSF.close()
        conn.close()

@app.route("/showSignIn")
def showSignIn():
    return render_template('signin.html')


@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


@app.route("/signUp", methods=['POST','GET'])
def signUp():
    try:
        #Read sign up form user input values
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        #Make sure user entered all of the values
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()

            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error = 'Wrong Email or Password')
        else:
            return render_template('error.html', error = 'Wrong Email or Password')

    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


"""
============================ACCOUNT============================
"""
@app.route('/showAddAccount')
def showAddAccount():
    return render_template('addAccount.html')


@app.route('/addAccount', methods=['POST'])
def addAccount():
    try:
        _account_name = request.form['inputName']
        _account_ammount = request.form['inputAmount']
        _user = session.get('user')

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_addAccount',(_user, _account_name, _account_ammount))
        data = cursor.fetchall()

        if len(data) is 0:
            #for game state of account
            userAccount.add_account(_account_name, _account_ammount)
            #
            #   MIGHT CHANGE THIS TO SUCCESSFULLY ADDED EXPENSE PAGE OR REDIRECT TO SHOW EXPENSES TABLE PAGE
            #
            conn.commit()
            return redirect('/showAccounts')
        else:
            return render_template('error.html', error = 'Error ocurred posting account')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/showAccounts')
def showAccounts():
    if session.get('user'):
        return render_template('showAccounts.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/getAccounts')
def getAccounts():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getAccountByUser', (_user,))
            accounts = cursor.fetchall()

            temp_dict = []
            accounts_dict = []
            if not userAccount.return_user_accounts():
                for account in accounts:
                    userAccount.add_account(account[2], account[3])

            temp_dict = userAccount.return_user_accounts()
            #This addition helps resolve creating the dict into a readable json format
            for account in temp_dict:
                accounts_dict.append({
                        'account': str(account.get('account')),
                        'saved':   str(account.get('saved'))
                })

            return json.dumps(accounts_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

"""
============================EXPENSE============================
"""

@app.route('/showAddExpense')
def showAddExpense():
    return render_template('addExpense.html')


@app.route('/addExpense', methods=['POST'])
def addExpense():
    try:
        _category = request.form['inputCategory']
        _cost = request.form['inputCost']
        _date = request.form['inputDate']
        _account = request.form['inputAccount']
        _user = session.get('user')

        #This part is messy and needs to be updated to be more coherent I needed a way to update Account amount
        #so I called several stored procedures to do so. This is slow and I can change this to one or two stored
        #procedures
        conn = mysql.connect()
        conn2 = mysql.connect()
        cursor1 = conn.cursor()
        cursor2 = conn.cursor()
        cursor3 = conn2.cursor()
        cursor4 = conn.cursor()

        cursor1.callproc('sp_getAccountIDByAccountName', (_user, _account))
        account_id = cursor1.fetchall()

        cursor2.callproc('sp_addExpense',(_user, _category, _cost, _date, account_id[0][0]))
        data = cursor2.fetchall()

        cursor4.callproc('sp_getAccountByUser', (_user,))
        accountData = cursor4.fetchall()

        if len(data) is 0:
            userLedger.add_expense(_cost, _category, _date, _account)
            #Deduct target account
            userAccount.deduct_expense(_cost, _account)
            oldAmount = newAmount = 0
            for accounts in accountData:
                if accounts[2] == _account:
                    oldAmount = accounts[3]

            newAmount = oldAmount - _cost

            cursor3.callproc('sp_updateAccount', (_account, newAmount, _user, account_id[0][0]))
            data2 = cursor3.fetchall()

            conn.commit()
            if len(data2) is 0:
                conn2.commit()

            return redirect('/showAddExpense')
        else:
            return render_template('error.html', error = 'Error ocurred posting account')
    except Exception as e:
        return render_template('error.html', error = str(e))
    finally:
        cursor1.close()
        cursor2.close()
        conn.close()


@app.route('/showExpenses')
def showExpenses():
    if session.get('user'):
        return render_template('showExpenses.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/getExpenses')
def getExpenses():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getExpenseByUser', (_user,))
            expenses = cursor.fetchall()

            temp_dict = []
            expense_dict = []

            temp_dict = userLedger.return_user_expenses()
            #This addition helps resolve creating the dict into a readable json format
            for expense in temp_dict:
                expense_dict.append({
                        'category': str(expense.get('category')),
                        'cost':     str(expense.get('cost')),
                        'date':     str(expense.get('date'))
                })

            return json.dumps(expense_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))

"""
============================INCOME============================
"""
@app.route('/showIncomes')
def showIncomes():
    if session.get('user'):
        return render_template('showIncomes.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/showAddIncome')
def showAddIncome():
    return render_template('addIncome.html')


@app.route('/getIncomes')
def getIncomes():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getIncomeByUser', (_user,))
            incomes = cursor.fetchall()

            temp_dict = []
            incomes_dict = []

            temp_dict = userAccount.return_user_incomes()

            #This addition helps resolve creating the dict into a readable json format
            for income in temp_dict:
                incomes_dict.append({
                        'paid':              str(income.get('paid')),
                        'ttype':             str(income.get('ttype')),
                        'frequency':         str(income.get('frequency')),
                        'payday':            str(income.get('payday')),
                        'deposit_account':   str(income.get('deposit_account'))
                })

            return json.dumps(incomes_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/addIncome', methods=['POST'])
def addIncome():
        try:
            _type = request.form['inputTitle']
            _paid = request.form['inputPaid']
            _frequency = request.form['inputFreq']
            _date = request.form['inputDate']
            _account = request.form['inputAccount']
            _user = session.get('user')

            conn = mysql.connect()
            cursor1 = conn.cursor()
            cursor2 = conn.cursor()

            cursor1.callproc('sp_getAccountIDByAccountName', (_user, _account))
            account_id = cursor1.fetchall()

            cursor2.callproc('sp_addIncome',(_user, account_id[0][0], _type, _paid, _date, _frequency))
            data = cursor2.fetchall()

            if len(data) is 0:
                userAccount.add_income(_paid, _type, _frequency, _date, _account)

                conn.commit()
                return redirect('/showAddIncome')
            else:
                return render_template('error.html', error = 'Error ocurred posting account')
        except Exception as e:
            return render_template('error.html', error = str(e))
        finally:
            cursor1.close()
            cursor2.close()
            conn.close()
"""
==========================DEDUCTION============================
"""

@app.route('/showDeductions')
def showDeductions():
    if session.get('user'):
        return render_template('showDeductions.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/showAddDeduction')
def showAddDeduction():
    return render_template('addDeduction.html')


@app.route('/getDeductions')
def getDeductions():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getDeductionByUser', (_user,))
            deductions = cursor.fetchall()

            temp_dict = []
            deductions_dict = []

            temp_dict = userAccount.return_user_deductions()

            #This addition helps resolve creating the dict into a readable json format
            for deduction in temp_dict:
                deductions_dict.append({
                        'amount':           str(deduction.get('amount')),
                        'type':             str(deduction.get('type')),
                        'frequency':        str(deduction.get('frequency')),
                        'date':             str(deduction.get('date')),
                        'deduct_account':   str(deduction.get('deduct_account'))
                })

            return json.dumps(deductions_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/addDeduction', methods=['POST'])
def addDeduction():
        try:
            _type = request.form['inputTitle']
            _amount = request.form['inputAmount']
            _frequency = request.form['inputFreq']
            _date = request.form['inputDate']
            _account = request.form['inputAccount']
            _user = session.get('user')

            conn = mysql.connect()
            cursor1 = conn.cursor()
            cursor2 = conn.cursor()

            cursor1.callproc('sp_getAccountIDByAccountName', (_user, _account))
            account_id = cursor1.fetchall()

            cursor2.callproc('sp_addDeduction',(_user, _type, _frequency, _amount, _date, account_id[0][0]))
            data = cursor2.fetchall()

            if len(data) is 0:
                userAccount.add_deduction(_amount, _type, _frequency, _date, _account)

                conn.commit()
                return redirect('/showAddDeduction')
            else:
                return render_template('error.html', error = 'Error ocurred posting account')
        except Exception as e:
            return render_template('error.html', error = str(e))
        finally:
            cursor1.close()
            cursor2.close()
            conn.close()

"""
============================SAVE+FOR============================
"""
@app.route('/showSaveFor')
def showSaveFor():
    if session.get('user'):
        return render_template('showSaveFor.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/showAddSaveFor')
def showAddSaveFor():
    return render_template('addSaveFor.html')


@app.route('/getSaveFor')
def getSaveFor():
    try:
        if session.get('user'):
            _user = session.get('user')

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getSFByUser', (_user,))
            sfs = cursor.fetchall()

            temp_dict = []
            sfs_dict = []

            temp_dict = userAccount.return_save_for()
            print("Hello World")
            #This addition helps resolve creating the dict into a readable json format
            for sf in temp_dict:

                #answer, netAmount = userAccount.save_for_reasonability(sf, userLedger)

                sfs_dict.append({
                        'desire':           str(sf.get('desire')),
                        'cost':             str(sf.get('cost')),
                        'date':             str(sf.get('date')),
                        'deduct_account':   str(sf.get('deduct_account'))
                })

            return json.dumps(sfs_dict)

        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/addSaveFor', methods=['POST'])
def addSaveFor():
        try:
            _desire = request.form['inputTitle']
            _cost = request.form['inputCost']
            _date = request.form['inputDate']
            _account = request.form['inputAccount']
            _start_date = request.form['inputStartDate']
            _user = session.get('user')

            conn = mysql.connect()
            cursor1 = conn.cursor()
            cursor2 = conn.cursor()

            cursor1.callproc('sp_getAccountIDByAccountName', (_user, _account))
            account_id = cursor1.fetchall()

            cursor2.callproc('sp_addSF',(_user, _date, _desire, _cost, account_id[0][0], _start_date))
            data = cursor2.fetchall()

            if len(data) is 0:
                userAccount.add_save_for(_desire, _date, _cost, _account, _start_date)

                conn.commit()
                return redirect('/showAddSaveFor')
            else:
                return render_template('error.html', error = 'Error ocurred posting account')
        except Exception as e:
            return render_template('error.html', error = str(e))
        finally:
            cursor1.close()
            cursor2.close()
            conn.close()


"""
==========================STATISTICS============================
"""
@app.route('/showStats')
def showStats():
    if session.get('user'):
        return render_template('showStats.html')
    else:
        return render_template('error.html', error = "Unauthorized user")


@app.route('/getStatsLinePlot')
def getStatsLinePlot():
        try:
            if session.get('user'):
                _user = session.get('user')
                line_plot_dict = []
                category_dict = []
                average = 0

                average, line_plot_data = userLedger.get_avg_weekly_spendings()
                ##Create the graph dictionary
                test_dict = []
                i = 0
                print(str(len(line_plot_data)))
                for i in range(len(line_plot_data)):
                    test_dict.append({
                                'X': str(i),
                                'Y': str(line_plot_data[i])
                    })


                return json.dumps(test_dict)

            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))

@app.route('/getStatsPieChart')
def getStatsPieChart():
        try:
            if session.get('user'):
                _user = session.get('user')

                pie_dict = []
                category_dict = []

                category_dict, pie_dict = userLedger.expense_statistics()
                ##Create the graph dictionary
                test_dict = []

                for pie_data in pie_dict:
                    test_dict.append({
                        'Y': str(pie_data.get('Average')),
                        'Label': str(pie_data.get('Category'))
                    })

                return json.dumps(test_dict)

            else:
                return render_template('error.html', error = 'Unauthorized Access')
        except Exception as e:
            return render_template('error.html', error = str(e))


@app.route('/addStats')
def addStats():
            try:
                if session.get('user'):
                    _user = session.get('user')


                    span_sums = []
                    wAverage = mAverage = 0

                    wAverage, span_sums = userLedger.get_avg_spendings('weekly')
                    mAverage, span_sums = userLedger.get_avg_spendings('month')
                    ##Create the graph dictionary
                    test_dict = []

                    test_dict.append({
                        'item': "Weekly Stats",
                        'category': "All Categories",
                        'span': "Weekly",
                        'average': str(wAverage)
                    })
                    test_dict.append({
                        'item': "Monthly Stats",
                        'category': 'All Categories',
                        'span': 'Monthly',
                        'average': str(mAverage)
                    })

                    return json.dumps(test_dict)

                else:
                    return render_template('error.html', error = 'Unauthorized Access')
            except Exception as e:
                return render_template('error.html', error = str(e))

"""
============================MAIN============================
"""

if __name__ == "__main__":
    app.run()
