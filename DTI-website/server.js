// Required modules
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser')

// Create Express app
const app = express()
const port = 3000
const jsonParser = bodyParser.json() // currently unused
const urlencodedParser = bodyParser.urlencoded({ extended: false })

const crowdData = require(path.join(__dirname, 'data', 'crowd.json'))

// Set up static file serving
app.use(express.static(path.join(__dirname, 'public')));
 
// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Define route for the homepage
app.get('/', (req, res) => {
    res.render('pages/index', {
        crowdLevels: crowdData.stations
    })
})

app.get('/choose-workout', (req, res) => {
  res.render('pages/form')
})

app.post( '/submit-workout', urlencodedParser, ( req, res ) => {
  console.log(req.body)
  res.redirect( 303, '/' )
})

// Start the server
app.listen(port, () => {
  console.log(`App listening at port ${port}`)
})

