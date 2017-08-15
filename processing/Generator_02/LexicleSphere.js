

function LexicleSphere(_x, _y, _size, _noise){
  //center x and y
  this.x = _x + _size; 
  this.y = _y + _size;
  this.radius = _size;
  this.diameter = this.radius * 2;
  
  //[{nerp:0, derp:0, herp:2}, {}...]
  this.noise = _noise; //array data object with keys equal to labels
  this.totalPoints = 150;
  
  //get min and max from the data
  this.dataMin = 0;
  this.dataMax = 1;
  this.borderData = {};
  
  for(var i=0; i < this.noise.length; i++){
      if(this.noise[i] > this.dataMax)
        this.dataMax = this.noise[i];
      if(this.noise[i] < this.dataMin)
        this.dataMin = this.noise[i];
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
  this.render = function(){
    
    this.drawLoop(this.noise, 'rgba(255,50,50, 0.75)');
    
  }
  
}