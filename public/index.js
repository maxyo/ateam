// Create app
const DATA = readJSON('../../php/src/faf7ef78-41b3-4a36-8423-688a61929c08.json');
const BAGS = readJSON('../../php/src/storage_1671921073.json');
const CLUSTERS = readJSON('../../php/src/clusters_1671921073.json');
const MOVIES = readJSON('../../php/src/moves_1671921073.json');

var width = window.innerWidth;
var height = window.innerHeight;

var stage = new Konva.Stage({
    container: 'container',
    width: width,
    height: height,
    draggable: true,
});
let layer = new Konva.Layer();
stage.add(layer);
// stage.container().style.backgroundColor = '';

calculatePaths();
calculateCluster()
// generateAreaCircle();

generateSquareNode({
    x: 0,
    y: 0,
    width: 10000,
    height: 10000,
    fill: '',
    stroke: 'black',
    strokeWidth: 4,
});

// склад
const base = {
    x: 0,
    y: 0,
    radius: 10,
    fill: 'green',
    stroke: 'black'
};
generateCircleNode(base);

//дети
DATA.children.map((item) => {
    item.radius = 1;
    item.fill = 'red';
    item.stroke = 'black';
    generateCircleNode(item);
});

let snow;
DATA.children.forEach((child, indexChild) => {
    snow = DATA.snowAreas.map((item, indexSnow) => {
        if ((item.x - child.x)*(item.x - child.x) + (item.y - child.y)*(item.y - child.y) <= item.r*item.r) {
            item.childs = item.childs ? item.childs+1 : 1;
        }
        return item;
    });
});

snow.map((item) => {
    item.radius = item.r;
    item.stroke = item.childs > 0 ? 'black' : 'red';
    generateCircleNode(item);
});

//снежные бури с детьми внутри
// console.log('asdasda',snow.sort((a, b) => a.childs > b.childs ? 1 : -1));

function generateAreaCircle()
{
    let x = 1000;
    while(true) {
        if (x >= 15000) break;
        generateWedgeNode({
            x: 0,
            y: 0,
            radius: x,
            angle: 90,
            fill: '',
            stroke: 'red',
            strokeWidth: 4,
            opacity: 1,
            rotation: 0,
        })
        x += 1000
    }
}

function calculatePaths() {
    let routes = MOVIES.map((arr)=> {
        //многомерный в одномерный [[], []] => []
        return [].concat(...arr);
    })
    let items = [];
    let route = [];
    routes.map((k)=> {
        items.push(k.x);
        items.push(k.y);
        if (k.x === 0 && k.y === 0) {
            route.push(items);
            items = [k.x, k.y];
        }
    })

    routes.map((r) => {
        const color = generateColor();
        let prev = r[0];
        const points = r.reduce((res, it, i) => {
            if (i % 2 === 1) {
                res.push({x: prev, y: it});
            } else {
                prev = it;
            }
            return res;
        }, []);

        let number = 1;
        points.forEach(p => {
            if(p.x === 0 && p.y === 0) {
                return;
            }
            generateNumber({
                text: `${number++}`,
                fill: color,
                stroke: color,
                strokeWidth: 1,
                x: p.x+2,
                y: p.y+2
            })
        })

        var poly = new Konva.Line({
            points: r,
            fill: generateColor(),
            stroke: color,
            strokeWidth: 1,
            opacity: 0.5,
            closed: false,
        });
        // add the shape to the layer
        layer.add(poly);
    })

}

function calculateCluster() {
    CLUSTERS.map((claster) => {
        let itemsX = [0],
            items = [],
            itemsY = [0];
        claster.map((i) => {
            itemsX.push(i.x)
            return i;
        }).map((i) => {
            itemsY.push(i.y)
        })

        itemsX.forEach((d, i) => {
            items.push(d),
                items.push(itemsY[i])
        })

        var poly = new Konva.Line({
            points: items,
            fill: generateColor(),
            stroke: 'black',
            strokeWidth: 0,
            opacity: 0.1,
            closed: true,
            bezier: false,
        });
        // add the shape to the layer
        layer.add(poly);
    })

}

function generateColor() {
    return '#' + Math.floor(Math.random()*16777215).toString(16)
}

function readJSON(file) {
    var request = new XMLHttpRequest();
    request.open('GET', file, false);
    request.send(null);
    if (request.status == 200)
        return JSON.parse(request.responseText);
}

function generateCircleNode(item) {
    layer.add( new Konva.Circle(item));
}
function generateSquareNode(item) {
    layer.add( new Konva.Rect(item));
}
function generateWedgeNode(item) {
    layer.add( new Konva.Wedge(item));
}
function generateNumber(item) {
    layer.add( new Konva.Text(item))
}
