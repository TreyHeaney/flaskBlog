from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author':   'Trey',
        'title':    'Developer Compensation Prediction App',
        'content':  """<h1>Abstract</h1>

I built a simple model around the  2020 Stack Overflow Developer Survey results in an attempt to predict developer compensations according to their qualifications and some other general personal information, and deployed a predictive interface for the model. 

The predictor was a ridge regression model boosted with a shallow random forest. 

The model obtained a final R^2 score of 0.44 and a mean absolute average of 32,000.'


Generate your own prediction here 

Process

     Pandas and sklearn were the primary preprocessors for our model, and a small amount was done manually. The data I used was the 2020 Stack Overflow Developer Survey results that was well prepared for preprocessing and modeling. The data consisted of 80k observations that I filtered down to about 7k. Non-US based developers were removed as were outliers in compensation.

The data consisted of columns of both categorical and numerical variables, so encoding of categorical values was required before modeling. I encoded the categorical values with onehot encoding which turns each categorical variable in a non-numeric column into an individual binary column,

Manual onehot in Pandas
Several columns included multiple variables in a single row for questions where multiple values are selected. I manually onehot encoded these with pandas. 

Imputation (replacing empty values) was also quickly done on the data. In this case, the means (in the case of continuous, number variables) and the mode (in the case of categorical variables) of every column replaced the empty values in that column. Imputation is necessary because complications caused by NaN-type values in python. 


     The model that generated metrics you will see here was a ridge regression model boosted with a shallow random forest regressor. A ridge regression is a simple regression that slightly underfits the training data so it generalizes better, and the booster was a shallow random forest that attempted to predict the residual of our ridge regression model. But the model you can interact with is a simple regression model boosted with the same method. It was significantly more easy to implement into an interactive app. 

Either model was generated using an sklearn pipeline chaining the preprocessors and the final predictor described above, and all and all there weren't many hiccups in the model generation process except modularizing the final model for the app.

I also implemented several hyperparameter searches, where many models with a range of different settings were created to see which settings performed the best with our model. 

I highly recommend checking out the python notebook if you're curious/want to learn about any of this because I've commented it in-depth for beginners. 


     The github repo deployed to heroku was mostly a template cloned from one of my teachers, modified for our use case. The HTML was written with dash, and much of the option selection frontend for our model was generated with a script similar to the one below. 
Not the exact script used


The output

The absolute gift of scripting! This saved me probably days of coding. 

More About The Input Data

Below is a list of the top 10 input columns that the model took sorted by importance to the model. I dropped many columns so the model generalizes better. In total, I used 43% of the original columns in the predictive model. I also limited the input of the interactive app to make it more friendly to use. """,
        'posted':   '11/24/2020',
        'type':		'project'
    },
    {
        'author':   'Trey',
        'title':    'This Blog',
        'content':  """""",
        'posted':   '11/24/2020',
        'type':		'project'
    },
    {
        'author':   'Trey',
        'title':    'My Thoughts',
        'content':  'I really think that we...',
        'posted':   '11/26/2020',
        'type':		'blog'
    },
]

blogs = [post for post in posts if post['type'] == 'blog']

projects = [post for post in posts if post['type'] == 'project']


@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    return render_template('home.html', posts=projects)
    

@app.route('/blog')
@app.route('/blog/')
def blog_page():
    return render_template('blog_page.html', title='Blog', posts=blogs)


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html', title='About')	
    

@app.route('/playground')
def play():
    return render_template('playground.html', title='Garbage')


app.run(debug=True)
