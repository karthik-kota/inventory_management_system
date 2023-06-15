import sqlite3
from flask import Flask, jsonify, request, render_template
#conn = sqlite3.connect('ims.db')

app = Flask(__name__)

def idgenerator(tab):
    conn = sqlite3.connect('ims.db')
    cur = conn.cursor()
    idval = ''
    if tab=='CUSTOMER':
        idval = 'CUSTOMER_ID'
    if tab=='PRODUCT':
        idval = 'PRODUCT_ID'
    if tab=='ORDERS':
        idval = 'ORDER_ID'
    if tab=='SUPPLIER':
        idval = 'SUPPLIER_ID'
    print(tab,idval)
    cur.execute(f"SELECT {idval} FROM {tab}")
    new = cur.fetchall()
    cud = str(new[len(new)-1][0])
    for i in range(len(str(cud))):
        if cud[i].isnumeric():
            f = i
            break
    myint = cud[f:]
    myint = int(myint)+1
    return idval[0:3]+str(myint)
print(idgenerator('CUSTOMER'))


# customer_name = 'rtf'
# customer_addr = 'hyd'
# customer_email = 'rtf@gmail.com'

# cn.execute('select * from customer')
# print(cn.fetchall())
# cn.execute(f"insert into customer (customer_name,customer_addr,customer_email) values('{customer_name}','{customer_addr}','{customer_email}')")
# conn.commit()

@app.route('/')
def home():
    return render_template('index.html')
#=================================Show customers===============================
@app.route("/show-customers")
def customer_show():
    conn = sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute('select * from customer')
    data=[]
    for i in cn.fetchall():
        customer={}
        customer['customer_id'] = i[0]
        customer['customer_name'] = i[1]
        customer['customer_addr'] = i[2]
        customer['customer_email'] = i[3]
        data.append(customer)
    print(data)
    return render_template('show-customer.html',data = data)

#=================================Show products===============================
@app.route("/show-products")
def product_show():
    conn = sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute('select * from product')
    data=[]
    for i in cn.fetchall():
        product={}
        product['product_id'] = i[0]
        product['product_name'] = i[1]
        product['stock'] = i[2]
        product['supplier_id'] = i[3]
        product['Price'] = i[4]
        data.append(product)
    print(data)
    return render_template('show-product.html',data = data)

#=================================Show Orders===============================
@app.route("/show-orders")
def order_show():
    conn = sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute('select * from orders')
    data=[]
    for i in cn.fetchall():
        order={}
        order['order_id'] = i[0]
        order['product_id'] = i[1]
        order['customer_id'] = i[2]
        order['customer_email'] = i[3]
        data.append(order)
    print(data)
    return render_template('show-order.html',data = data)

#=================================Show Suppliers===============================
@app.route("/show-suppliers")
def supplier_show():
    conn = sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute('select * from supplier')
    data=[]
    for i in cn.fetchall():
        supplier={}
        supplier['supplier_id'] = i[0]
        supplier['supplier_name'] = i[1]
        supplier['supplier_addr'] = i[2]
        supplier['supplier_email'] = i[3]
        data.append(supplier)
    print(data)
    return render_template('show-supplier.html',data = data)
#=================================INSERT DATA INTO CUSTOMER FROM WEB===============================================
@app.route("/add-customer",methods=['GET','POST'])
def addcustomer():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        id=idgenerator('CUSTOMER')
        cn=conn.cursor()
        customername=request.form.get('name')
        customeraddr=request.form.get('address')
        customeremail=request.form.get('email')
        cn.execute(f"insert into customer(customer_id,customer_name,customer_addr,customer_email) values('{id}','{customername}','{customeraddr}','{customeremail}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addcustomer.html')
    
#=================================UPDATE CUSTOMER DEATILS======================================
@app.route("/update-customer", methods=['GET','POST'])
def updatecustomer():    
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        customerid=request.form.get('customerid')
        change=request.form.get('change')
        print(customerid)
        print(change)
        newvalue = request.form.get('newvalue')
        print(newvalue)
        cn.execute(f"update customer set {change} = '{newvalue}' where customer_id = '{customerid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updatecustomer.html')
    
#===========================================INSERT DATA INTO PRODUCT=======================
@app.route("/add-product",methods=['GET','POST'])
def addproduct():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        id=idgenerator('PRODUCT')
        cn=conn.cursor()
        productname=request.form.get('name')
        stock=request.form.get('stock')
        supplierid=request.form.get('supplierid')
        price=request.form.get('price')
        cn.execute(f"insert into product(product_id,product_name,stock,supplier_id,price) values('{id}','{productname}','{stock}','{supplierid}','{price}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addproduct.html')
#============================================UPDATE DATA INTO PRODUCT========================
@app.route("/update-product", methods=['GET','POST'])
def updateproduct():    
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        productid=request.form.get('productid')
        change=request.form.get('change')
        print(productid)
        print(change)
        newvalue = request.form.get('newvalue')
        print(newvalue)
        cn.execute(f"update product set {change} = '{newvalue}' where product_id = '{productid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updateproduct.html')
#================================================INSERT DATA INTO ORDERS==================================
@app.route("/add-order",methods=['GET','POST'])
def addorder():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        id=idgenerator('ORDERS')
        #orderid=request.form.get('orderid')
        productid=request.form.get('productid')
        customerid=request.form.get('customerid')
        customeremail=request.form.get('customermail')
        cn.execute(f"insert into orders (order_id,product_id,customer_id,customer_email) values('{id}','{productid}','{customerid}','{customeremail}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addorder.html')
#=======================================UPDATE DATA INTO ORDERS================================
@app.route("/update-order", methods=['GET','POST'])
def updateorder():    
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        orderid=request.form.get('orderid')
        change=request.form.get('change')
        print(orderid)
        print(change)
        newvalue = request.form.get('newvalue')
        print(newvalue)
        cn.execute(f"update orders set {change} = '{newvalue}' where order_id = '{orderid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updateorder.html')
#================================DELETE DATA INTO ORDERS========================
# @app.route("/delete-supplier", methods=['GET','POST'])
# def deletesupplier():    
#     if request.method=='POST':
#         cn=conn.cursor()
#         supplierid=request.form.get('supplierid')
#         cn.execute(f"delete from supplier where supplier_id='{supplierid}'")
#         conn.commit()
#         print('Data as been Delete')
#         return jsonify({'message':'sucessfull'})
#     else:
#         return render_template('deletesupplier.html')
#================================INSERT DATA INTO SUPPLIER=======================
@app.route("/add-supplier",methods=['GET','POST'])
def addsupplier():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        id=idgenerator('SUPPLIER')
        #supplierid=request.form.get('supplierid')
        suppliername=request.form.get('suppliername')
        supplieraddr=request.form.get('supplieraddr')
        supplieremail=request.form.get('suppliermail')
        cn.execute(f"insert into supplier (supplier_id,supplier_name,supplier_addr,supplier_email) values('{id}','{suppliername}','{supplieraddr}','{supplieremail}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('addsupplier.html')
#================================UPDATE DATA OF SUPPLIER===========================
@app.route("/update-supplier", methods=['GET','POST'])
def updatesupplier():    
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        supplierid=request.form.get('supplierid')
        change=request.form.get('change')
        print(supplierid)
        print(change)
        newvalue = request.form.get('newvalue')
        print(newvalue)
        cn.execute(f"update supplier set {change} = '{newvalue}' where supplier_id = '{supplierid}'")
        conn.commit()
        print('Data as been Updated')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('updatesupplier.html')
#===============================DELETE DATA INTO SUPPLIER====================================
@app.route("/delete-supplier", methods=['GET','POST'])
def deletesupplier():    
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor() 
        supplierid=request.form.get('supplierid')
        cn.execute(f"delete from supplier where supplier_id='{supplierid}'")
        conn.commit()
        print('Data as been Delete')
        return jsonify({'message':'sucessfull'})
    else:
        cn=conn.cursor()
        cn.execute('select * from supplier')
        data=[]
        for j in cn.fetchall():
            supplier={}
            supplier['supplier_id'] = j[0]
            supplier['supplier_name'] = j[1]
            supplier['supplier_addr'] = j[2]
            supplier['supplier_email'] = j[3]  
            data.append(supplier)
        return render_template('deletesupplier.html',data=data)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = False)
