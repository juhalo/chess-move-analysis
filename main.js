function createElement(text, rightOrLeft, num) {
  let container;
  if (rightOrLeft == 'left') {
    container = document.querySelector('#main-left-content');
  } else {
    container = document.querySelector('#main-right-content');
  }
  const newDiv = document.createElement('div');
  newDiv.textContent = num + ': ' + text;
  container.appendChild(newDiv);
}

const whiteMoves = JSON.parse(
  '{"columns":["pvalue","include"],"index":["c4","f5","e5","d4","d6","h4","c5","f4","h5","f6","c6","g5","h6","b6","a5","b4","g6","a6","e4","e6","b5","g4","d5"],"data":[[0.0001736759,true],[0.0614528164,true],[0.0711097961,true],[0.0919339529,true],[0.0993470472,true],[0.1383667228,true],[0.1881439073,false],[0.2138505775,false],[0.2504204769,false],[0.3496345329,false],[0.3729440963,false],[0.4046840111,false],[0.4084525379,false],[0.4265779457,false],[0.4646609436,false],[0.4763701463,false],[0.4872520964,false],[0.4886968974,false],[0.4917616685,false],[0.7332003687,false],[0.7523722043,false],[0.8631410519,false],[0.9115196657,false]]}'
);
const blackMoves = JSON.parse(
  '{"columns":["pvalue","include"],"index":["b3","e4","h3","b5","f3","d3","c3","a4","g3","e5","d5","d4","g4","f4","h4","b4","f5","a5","g5","e3","c5","c4","h5"],"data":[[0.0009456999,false],[0.0020947473,true],[0.0023743428,false],[0.0159657164,true],[0.0375626106,false],[0.048081171,true],[0.0525820778,true],[0.0754120771,true],[0.0848254517,false],[0.241130361,false],[0.3417402403,false],[0.3545755604,false],[0.3907749168,false],[0.4728325445,false],[0.5630008057,false],[0.6223275054,false],[0.6267663077,false],[0.667676276,false],[0.7153437779,false],[0.7508093039,false],[0.8123517017,false],[0.8617190522,false],[0.934193165,false]]}'
);

let num = 1;

for (let i = 0; i < whiteMoves.index.length; i++) {
  if (whiteMoves['data'][i][1]) {
    createElement(whiteMoves.index[i], 'left', num);
    num++;
  }
}

num = 1;

for (let i = 0; i < blackMoves.index.length; i++) {
  if (blackMoves['data'][i][1]) {
    createElement(blackMoves.index[i], 'right', num);
    num++;
  }
}
