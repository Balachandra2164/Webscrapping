from flask import Flask, render_template,request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__) #creation of flask app with name as "app"

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            searchstring=request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchstring
            uClient=uReq(flipkart_url)
            flipkartpage=uClient.read()
            uClient.close()
            flipkart_html=bs(flipkartpage,"html.parser")
            bigboxes=flipkart_html.findAll("div",{"class":"bhgxx2 col-12-12"})
            del bigboxes[0:3]
            box=bigboxes[0]
            productlink="http://www.flipkart.com"+box.div.div.div.a['href']
            prodRes=requests.get(productlink)
            prodRes.encoding='utf-8'
            prod_html=bs(prodRes.text, "html.parser")
            #print(prod_html)
            comment_boxes=prod_html.find_all('div',{'class':'_3nrCtb'})
            filename=searchstring+".csv"
            fw=open(filename,'w')
            headers="Product, Customer Name,Rating, Heading,Comment \n"
            fw.write(headers)
            reviews=[]
            for commentbox in comment_boxes:
                try:
                    name=commentbox.div.div.find_all('p',{'class':"_3LYOAd _3sxSiS"})[0].text
                except:
                    name='No name'
                try:
                    rating=commentbox.div.div.div.div.text
                except:
                    rating="No Rating"
                try:
                    # commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag=commentbox.div.div.find_all('div',{'class':''})
                    # custComment.encode(encoding='utf-8')
                    custComment=comtag[0].text
                except Exception as e:
                    print('Exception while creating dictionary:',e)
                my_dict={"Product": searchstring, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(my_dict)
            return render_template('results.html',reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print("The excemption error message is",e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)