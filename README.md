# kivy-money-stat-report-app
An application that allows you to analyse money that you've spent and gained during a defined amount of time by showing a pie chart graph of moeny you've spent or gained grouped by 'reason'; a plot of the cumsum of the money spent; gained;rest; along a period of time(based on the data)

This application was built using python which is; obviously the most suitable programming language for data science and it has also andvatage on GUI by using kivy;

I also choose python because I'm a data scientist; 
The more practice the better

During this project, I encountered many problems, such as: adding matplotlib graphs in kivy, because matlplotlib is a backend module; so it cannot be implemented directly using the common method; but there is, of course a solution, which is using FigureCanvasKivyAgg from from kivy.garden.matplotlib.backend_kivyagg package

This project is still in development however it is already ready to use


## Requirement and installation

this application uses some modules that need to be installed, like: *pandas*, *numpy*, *matplotlib*, *kivy*, *kivy-garden*

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install these

```bash

pip install pandas numpy matplotlib kivy

```

If *pip* is not installed, please install it in your system:


```bash

sudo apt install python3-pip

```

For windows, download the [python interpreter](https://www.python.org/)

To verify that the modules is successfully installed use the command:

```bash

pip list

```

It will return the list of modules and packages installed on your system

## How to use

After installing all required modules and cloning the app on your repo, run the app using the command:

```bash

python moneyApp.py

```

or 

```bash

python3 moneyApp.py

```
