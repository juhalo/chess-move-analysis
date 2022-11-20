function createElement(text, rightOrLeft, num) {
  let container;
  if (rightOrLeft == 'left') {
    container = document.querySelector('#main-left-content');
  } else {
    container = document.querySelector('#main-right-content');
  }
  const newDiv = document.createElement('div');
  newDiv.textContent = num + '. ' + text;
  container.appendChild(newDiv);
}

const whiteMoves = JSON.parse(
  '{"columns":["Moves","P"],"index":[9,4,11,6,10,0,7,2,3,13,1,14,15,12,5,8],"data":[["e5",0.026866751],["c4",0.0453989594],["f5",0.0460479373],["d4",0.0518393946],["f4",0.0711884594],["a4",0.091514556],["d5",0.0959632875],["b4",0.1849129984],["b5",0.2873830569],["g5",0.2992517595],["a5",0.6126947605],["h4",0.6601363093],["h5",0.6998122512],["g4",0.7489485561],["c5",0.9587207254],["e4",0.9592896907]]}'
);
const blackMoves = JSON.parse(
  '{"columns":["Moves","P"],"index":[8,7,13,14,9,12,1,6,10,5,4,11,3,2,0,15],"data":[["e4",0.1233148878],["d5",0.204664169],["g5",0.2196721287],["h4",0.2274870995],["e5",0.262343611],["g4",0.3391631306],["a5",0.4172366049],["d4",0.4384556709],["f4",0.4590458722],["c5",0.5382558618],["c4",0.6629399856],["f5",0.7123441276],["b5",0.7399934773],["b4",0.7487691906],["a4",0.7596114317],["h5",0.9215477725]]}'
);

let num = 1;
for (const move of whiteMoves['data']) {
  if (move[1] < 0.15) {
    createElement(move[0], 'left', num);
    num++;
  }
}

num = 1;
for (const move of blackMoves['data']) {
  if (move[1] < 0.15) {
    createElement(move[0], 'right', num);
    num++;
  }
}
