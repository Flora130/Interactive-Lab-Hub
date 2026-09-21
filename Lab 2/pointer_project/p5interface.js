
let activeRegion = 1;
let pointerLengths = [0, 0, 0, 0];
let pointerGrowing = [false, false, false, false];

// Maximum length of each pointer
let maxPointerLength = 260;
let growthSpeed = 0.5;



function setup() {
  createCanvas(600, 600);
  angleMode(DEGREES);
}


function draw() {

  background(240);

  fill(
    activeRegion === 1
      ? color(255, 150, 180)
      : color(210, 180, 190)
  );

  noStroke();

  rect(
    0,
    0,
    width / 2,
    height / 2
  );



  fill(
    activeRegion === 2
      ? color(150, 200, 245)
      : color(180, 195, 210)
  );

  rect(
    width / 2,
    0,
    width / 2,
    height / 2
  );



  fill(
    activeRegion === 3
      ? color(150, 215, 160)
      : color(180, 195, 185)
  );

  rect(
    0,
    height / 2,
    width / 2,
    height / 2
  );


  fill(
    activeRegion === 4
      ? color(255, 225, 120)
      : color(230, 225, 190)
  );

  rect(
    width / 2,
    height / 2,
    width / 2,
    height / 2
  );




  fill(40);

  textAlign(CENTER, CENTER);

  textSize(56);

  text(
    "HOME",
    150,
    150
  );

  text(
    "SCHOOL",
    450,
    150
  );

  text(
    "GYM",
    150,
    450
  );

  text(
    "OUTDOOR",
    450,
    450
  );


  let index = activeRegion - 1;

  if (pointerGrowing[index]) {

    pointerLengths[index] += growthSpeed;

    // Stop automatically at maximum length
    if (pointerLengths[index] >= maxPointerLength) {

      pointerLengths[index] = maxPointerLength;

      pointerGrowing[index] = false;
    }
  }


  drawAllPointers();


  fill(30);

  noStroke();

  circle(
    width / 2,
    height / 2,
    40
  );

  fill(40);

  textAlign(CENTER, CENTER);

  textSize(20);

  text(
    "1 Home   2 School   3 Gym   4 Outdoor",
    width / 2,
    550
  );

  text(
    "Q Start / Continue     W Stop",
    width / 2,
    580
  );
}



function drawAllPointers() {

  drawPointer(
    1,
    225
  );



  drawPointer(
    2,
    315
  );



  drawPointer(
    3,
    135
  );



  drawPointer(
    4,
    45
  );
}



function drawPointer(region, angle) {

  let index = region - 1;

  let centerX = width / 2;
  let centerY = height / 2;

  let length = pointerLengths[index];


  // If this pointer has never been activated,
  // don't draw it.
  if (length <= 0) {
    return;
  }


  // Calculate pointer endpoint
  let endX =
    centerX +
    cos(angle) * length;

  let endY =
    centerY +
    sin(angle) * length;


  stroke(30);

  strokeWeight(12);

  strokeCap(ROUND);

  line(
    centerX,
    centerY,
    endX,
    endY
  );


  fill(30);

  noStroke();

  circle(
    endX,
    endY,
    24
  );
}


function keyPressed() {

  if (key === '1') {
    activeRegion = 1;
  }

  if (key === '2') {
    activeRegion = 2;
  }

  if (key === '3') {
    activeRegion = 3;
  }

  if (key === '4') {
    activeRegion = 4;
  }



  if (key === 'q' || key === 'Q') {

    let index = activeRegion - 1;


    pointerGrowing[index] = true;
  }



  if (key === 'w' || key === 'W') {

    let index = activeRegion - 1;

    // Stop the pointer,
    // but keep its current length.

    pointerGrowing[index] = false;
  }
}
