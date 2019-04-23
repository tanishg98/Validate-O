var busboy = require('connect-busboy'); //middleware for form/file upload
var path = require('path');     //used for file path
var fs = require('fs-extra');       //File System - for file manipulation
var cors = require('cors');
var express = require('express');
var PythonShell = require('python-shell');

module.exports = (app) => {
  app.use(cors());
  app.options('*', cors());
  app.use(busboy());
  app.use(express.static(path.join(__dirname, 'public')));

  /* ==========================================================
Create a Route (/upload) to handle the Form submission
(handle POST requests to /upload)
Express v4  Route definition
============================================================ */
app.route('/upload')
    .post(function (req, res, next) {
        console.log(req.query);
        var fstream;
        req.pipe(req.busboy);
        req.busboy.on('file', function (fieldname, file, filename) {
            console.log("Uploading: " + filename);

            //Path where image will be uploaded
            fstream = fs.createWriteStream(__dirname + '/uploads/' + 'image.jpg');
            file.pipe(fstream);
            fstream.on('close', function () {
                console.log("Upload Finished of " + filename);
                var python = require('child_process').spawn(
                 'python',
                 // second argument is array of parameters, e.g.:
                 [`${__dirname}/${req.query.id}.py`]
                 );
                 var output = "";
                 python.stdout.on('data', function(data){ output += data });
                 console.log(output);
                 python.on('close', function(code){
                   console.log(code);
                   if (code !== 0) {
                       return res.send(500, code);
                   }
                   return res.send(200, output);
                 });
            });
        });
    });

    app.get('/get_image', (req,res) => {
      fs.readFile(__dirname + '/uploads/' + 'image.jpg', function (err, content) {
        if (err) {
            res.writeHead(400, {'Content-type':'text/html'})
            console.log(err);
            res.end("No such image");
        } else {
            //specify the content type in the response will be an image
            res.writeHead(200,{'Content-type':'image/jpg'});
            res.end(content);
        }
      });
    });

}