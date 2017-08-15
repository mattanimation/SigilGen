

function RadarChart(_x, _y, _size, _sets){
  //center x and y
  this.x = _x + _size; 
  this.y = _y + _size;
  this.radius = _size;
  this.diameter = this.radius * 2;
  
  //[{nerp:0, derp:0, herp:2}, {}...]
  this.dataSets = _sets; //array data object with keys equal to labels
  this.totalPoints = Object.keys(this.dataSets[0]).length;
  this.labels = Object.keys(this.dataSets[0]);
  
  //get min and max from the data
  this.dataMin = 0;
  this.dataMax = 1;
  this.borderData = {};
  
  for(var i=0; i < this.dataSets.length; i++){
    var kz = Object.keys(this.dataSets[i]);
    for(var j=0; j < kz.length; j++){
      this.labels.push(kz[j]);
      this.borderData[kz[j]] = 0; //populate border data with same keys but flat data
      if(this.dataSets[i][kz[j]] > this.dataMax)
        this.dataMax = this.dataSets[i][kz[j]];
      if(this.dataSets[i][kz[j]] < this.dataMin)
        this.dataMin = this.dataSets[i][kz[j]];
    }
  }
  //set border data to all max values
  var bdrKeys = Object.keys(this.borderData);
  for(var j=0; j < bdrKeys.length; j++){
    this.borderData[bdrKeys[j]] = this.dataMax;
  }
  
  //render labels and border with max values
  this.drawBorder = function(_data){
    
    //draw points and labels
    var dataScale = 0.5;
    
    stroke(0);
    strokeWeight(2);
    beginShape();
    noFill();
    
    var x,y, theta, angle, distFromCenter = 0;
    var setKeys = Object.keys(_data);
    //draw the border
    for(var j=0; j < setKeys.length; j++){
      var thisKey = setKeys[j];
      
      theta = (TWO_PI / (setKeys.length)); // -1 makes it go full circle with line
      angle = (theta * j);
     
      //normalize the data so that the max is the radius of the circle
      //normalize and add scaling
      distFromCenter = ( map(_data[thisKey], this.dataMin, this.dataMax, 0, this.diameter) * dataScale);
      //console.log(distFromCenter +" " +angle +" " +theta);
     
      x = this.x + (distFromCenter * cos(angle)) - (this.radius);
      y = this.y + (distFromCenter * sin(angle)) - (this.radius);
      //console.log(x, y);
      //draw line from center out
      //line(this.x, this.y, x, y);
      //draw point
      vertex(x,y);
      //draw label
      fill(0);
      textSize(24);
      text(setKeys[j], x,y);
      noFill();
    }
   
    endShape(CLOSE);
  }
  
  //given an array of data, draw points and lines
  this.drawLoop = function(_dataPoints, _color){
    //draw points and labels
    var dataScale = 0.5;
    console.log("drawing loop");
    
    noStroke();
    beginShape();
    fill(_color);
    
    var x,y, theta, angle, distFromCenter = 0;
    
    for(var j=0; j < _dataPoints.length; j++){
      theta = (TWO_PI / (_dataPoints.length)); // -1 makes it go full circle with line
      angle = (theta * j);
     
      //normalize the data so that the max is the radius of the circle
      //normalize and add scaling
      distFromCenter = ( map(_dataPoints[j], this.dataMin, this.dataMax, 0, this.diameter) * dataScale);
      console.log(distFromCenter +" " +angle +" " +theta);
     
      x = this.x + (distFromCenter * cos(angle)) - (this.radius);
      y = this.y + (distFromCenter * sin(angle)) - (this.radius);
      console.log(x, y);
      //draw line from center out
      //line(this.x, this.y, x, y);
      //draw point
      vertex(x,y);
      
    }
        
    smooth();
    endShape(CLOSE);
  }
  
  //draw the chart
  this.render = function(renderBackground){
    //render external border by using first dataset
    if(renderBackground)
      this.drawBorder(this.borderData);
    //blendMode(MULTIPLY);
    var a = (1.0 / this.dataSets.length);
    //create colors
    var colors = [];
    for(var i=0; i < this.dataSets.length; i++)
    {
      var r = Math.round(Math.random(10,255));
      var g = Math.round(Math.random(10,255));
      var b = Math.round(Math.random(10,255));
      colors.push('rgba('+r+','+g+','+b+','+a+')');
    }
    
    for(var i=0; i < this.dataSets.length; i++){
        var thisSet = this.dataSets[i];
        var vals = [];
        var kz = Object.keys(this.dataSets[i]).forEach(function(v){vals.push(thisSet[v]);});
        //console.log("vals: ", vals, colors[i]);
        this.drawLoop(vals, colors[i]);
    }
    
  }
  
}