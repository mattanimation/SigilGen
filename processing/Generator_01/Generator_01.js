
function setup() {
  // Sets the screen to be 720 pixels wide and 400 pixels high
  createCanvas(640, 640);
  background(255);
  colorMode(HSB, 360, 100, 100);
  noStroke();

  fill(0);
  //noFill();
  var startX = 320;
  var startY = 320;
  var dst = 50;
  var scl = 10;
  var totalPoints = 150; //num points around circle
  var randomData = new Array(0);
  var z=0;
  for(var i =0; i < totalPoints; i++){ 
    randomData.push(sin(z) + 2);
    z += random(0,0.5);
  }
  var dataScale = 4;
  var circleRad = 100; //radius size of circle
  strokeWeight(2);
  strokeJoin(ROUND);
  beginShape();
  var x,y=0;
  //drw graph around circle
  for(var i=0; i < totalPoints; i++){
    //pos plus random noise
    var theta = (TWO_PI / (totalPoints - 1)); //the -1 makes it goes full circle
    var angle = (theta * i);
    var dataOffset = (randomData[i] * dataScale);
    var distFromCenter = circleRad + dataOffset;
    x= startX + ( distFromCenter * cos(angle)); 
    y= startY + ( distFromCenter * sin(angle));
    //draw point
    //ellipse(x, y, 3, 3);
    //stroke(150);
    //var a = atan2(y, x);
    //draw line
    line(startX, startY, x, y);
    //noStroke();
    vertex(x,y);
  }
  smooth();
  endShape(CLOSE);

  //fill(150);
  noStroke();
 
  var h = random(0, 360);
  var rr = circleRad * 2;
  
  for (var r = rr; r > 0; -r) {
    fill(h, 90, 90);
    ellipse(startX, startY, r, r);  
    h = (h + 1) % 360;
  }

  noFill();
  stroke(0);
  triangle(startX - (circleRad /2), startY + (circleRad /2), startX, startY - (circleRad), startX + (circleRad / 2), startY + (circleRad /2));

}