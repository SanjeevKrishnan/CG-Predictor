from flask import Flask,render_template,request
import numpy as np
import itertools

def calc_CG(cg_present, credit_present, n, credit, grade):
	credit_array = np.array(credit,dtype = int)
	grade_array = np.array(grade,dtype = int)
	choice = np.empty(shape = n,dtype = int)
	choice_final = [None] * n
	max_cg = cg_present
	sg = 0.0
	all_choice = np.array(list(itertools.product([0,1],repeat=n)),dtype=int)

	product_present = cg_present*credit_present

	for i in range(2**n):
		credit_considered = np.multiply(credit_array,all_choice[i])
		product_new = np.multiply(credit_considered,grade_array)
		sg_tmp = np.sum(product_new)/np.sum(credit_considered)
		cg_new_tmp = (product_present+np.sum(product_new))/(credit_present+np.sum(credit_considered))
		if(cg_new_tmp>=max_cg):
			choice = all_choice[i]
			max_cg = cg_new_tmp
			sg = sg_tmp

	for i in range(n):
		if(choice[i]):
			choice_final[i] = 'Course '+str(i+1)+': Letter Grade'
		else:
			choice_final[i] = 'Course '+str(i+1)+': Satisfactory'

	return round(max_cg,3), round(sg,3), choice_final


app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/submitMain",methods=["POST"])
def submitMain():
	cg_present = float(request.form['inputCGPresent'])
	credit_present = int(request.form['inputTECR'])
	n = int(request.form['inputn'])
	inputCredit = [None] * n
	inputGrade = [None] * n

	for i in range(n):
		inputCredit[i] = int(request.form['inputCredit'+str(i+1)])
		inputGrade[i] = int(request.form['inputGrade'+str(i+1)])

	max_cg, sg, choice_final = calc_CG(cg_present = cg_present, credit_present = credit_present, n = n, credit = inputCredit, grade = inputGrade)

	return render_template('final.html', value = max_cg, var1 = sg, l= choice_final)


if __name__ == "__main__":
	app.run() 