from application import db
from application.accounts.forms import AccountDetailsForm, SearchAccountForm, AccountConfirmationForm, DepositMoneyForm, WithdrawMoneyForm, TransferMoneyForm, PrintStatementForm
from application.models import Customer, Account
from flask import render_template, redirect, flash, url_for, session, Blueprint
from application.utils import searchAccount, depositMoney, withdrawMoney, transferMoney


accounts = Blueprint('accounts', __name__)


#============================================Create New Account=======================================#
@accounts.route("/create_account",methods=["GET","POST"])
def create_account():
	if session.get('ROLE') != "acc_exec":
		flash("Action Not Allowed", category="danger")
		return redirect('main.home')
	else:
	    form = AccountDetailsForm()
	    form.acc_no.data = Account.generate_acc_no()
	    if form.validate_on_submit():
	        account = Account(acc_no=form.acc_no.data, acc_balance=form.acc_balance.data, acc_type=form.acc_type.data, cust_id=form.cust_id.data)
	        db.session.add(account)
	        db.session.commit()
	        flash("Account Successfully Created!!!", category="success")
	        return redirect(url_for('main.home'))
	    return render_template("accounts/create_account.html",form=form, title="Create Account")

#============================================Delete Account=======================================#
@accounts.route("/delete_account/<int:acc_no>",methods=["GET","POST"])
def delete_account(acc_no):
	account = Account.query.filter_by(acc_no=acc_no).first()
	form = AccountConfirmationForm()
	if form.validate_on_submit():
		if form.confirm.data and form.acc_no.data == acc_no:
			db.session.delete(account)
			db.session.commit()
			flash("Account Successfully Deleted!!!", category="success")
			return redirect(url_for('main.home'))
		elif (not form.confirm.data) or (form.acc_no.data != acc_no):
			flash("Wrong input data!!!", category="danger")
			return redirect(url_for('main.home'))
	return render_template('accounts/delete_confirmation_form.html', title="Confirm Delete", form=form, acc_no=acc_no)

#============================================Search Account=======================================#
@accounts.route("/search_account",methods=["GET","POST"])
def search_account():
	form = SearchAccountForm()
	if form.validate_on_submit():
		account = searchAccount(acc_no=form.acc_no.data, cust_id=form.cust_id.data, acc_type=form.acc_type.data)
		if account == None:
			flash("Acount not found...", category="danger")
			return redirect(url_for('main.home'))
		else:
			return render_template('accounts/show_account_details.html', account=account, title="Show Account Details")
	return render_template('accounts/search_account.html', form=form, title="Search Account")


#============================================Deposite Money=======================================#
@accounts.route("/deposit/<int:acc_no>",methods=["GET","POST"])
def deposit(acc_no):
	form = DepositMoneyForm()
	account = searchAccount(acc_no=acc_no)
	if form.validate_on_submit():
		result = depositMoney(depositAmount=form.depositAmount.data, acc_no=acc_no)
		if result == "Success":
			flash("Amount Successfully Deposited...", category="success")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Deposited...", category="danger")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
	return render_template("accounts/deposit.html",title="Deposit Money", account=account, form=form)


#============================================Withdraw Money=======================================#
@accounts.route("/withdraw/<int:acc_no>",methods=["GET","POST"])
def withdraw(acc_no):
	form = WithdrawMoneyForm()
	account = Account.query.filter_by(acc_no=acc_no).first()
	if form.validate_on_submit():
		result = withdrawMoney(withdrawAmount=form.withdrawAmount.data, acc_no=acc_no)
		if result == "Success":
			flash("Amount Successfully withdrawn...", category="success")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Withdrawn...", category="danger")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
	return render_template("accounts/withdraw.html",title="Withdraw Money", account=account, form=form)

#============================================Transfer Money=======================================#
@accounts.route("/transfer/<int:acc_no>",methods=["GET","POST"])
def transfer(acc_no):
	form = TransferMoneyForm()
	account = searchAccount(acc_no=acc_no)
	if form.validate_on_submit():
		print(form.amount.data, account.cust_id, form.from_acc.data, form.to_acc.data)
		result = transferMoney(amount=form.amount.data, cust_id=account.cust_id, from_acc=form.from_acc.data, to_acc=form.to_acc.data)
		if result == "Success":
			flash("Amount Successfully Transfered...", category="success")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
		else:
			flash("Amount Not Transfered...", category="danger")
			return redirect(url_for('main.show_account_details', acc_no=account.acc_no))
	return render_template("accounts/transfer.html",title="Transfer Money", account=account, form=form)

#============================================Account Statement=======================================#
@accounts.route("/acc_statement/<int:acc_no>",methods=["GET","POST"])
def acc_statement(acc_no):
	form = PrintStatementForm()
	account = Account.query.filter_by(acc_no=acc_no).first()
	customer = Customer.query.filter_by(cust_id=account.cust_id).first()
	if form.validate_on_submit():
		if form.choice.data == 'LT':
			transactions = customer.transactions
			transactions = transactions[-form.no_of_transactions.data:]
			return render_template('accounts/show_transactions.html', transactions=transactions, title="Account Statement", account=account)
		elif form.choice.data == 'BD':
			transactions = customer.transactions
			statement_transactions = []
			for transaction in transactions:
				if transaction.transaction_date >= form.from_date.data and transaction.transaction_date <= form.to_date.data:
					statement_transactions.append(transaction)
			return render_template('accounts/show_transactions.html', transactions=statement_transactions, title="Account Statement", account=account)
	return render_template("accounts/acc_statement.html",title="Account Statement", form=form, acc_no=acc_no)
	
