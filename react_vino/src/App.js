import React,{Component} from 'react';

class App extends Component{
  constructor(props){
    super(props);


    const sock = new WebSocket("ws://localhost:8081/audio");
    sock.binaryType = "blob";

    sock.onopen = () =>{
      console.log("sock start");
    }

    
    var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    var myArrayBuffer = audioCtx.createBuffer(1, 512 * 2, 44100);
    


    sock.onmessage = e => {
      // for (var channel = 0; channel < 1; channel++) {
      // //   // This gives us the actual ArrayBuffer that contains the data
      //   var nowBuffering = myArrayBuffer.getChannelData(channel);
      //   for (var i = 0; i < e.data.length; i++) {
      // //     // Math.random() is in [0; 1.0]
      // //     // audio needs to be in [-1.0; 1.0]
      //      nowBuffering[i] = Math.random() * 2 - 1;
      //    }
      //  }
      //  var source = audioCtx.createBufferSource();
      //  source.buffer = e.data;
      //  source.connect(audioCtx.destination);
      //  source.start();
      e.data.arrayBuffer().then(data => {
        const data16Arr = new Float32Array(data);
        //console.log(data16Arr)
        for (var channel = 0; channel < 1; channel++) {
          var nowBuffering = myArrayBuffer.getChannelData(channel);
          //buffer = count === 0 ? myArrayBuffer : appendBuffer(buffer, myArrayBuffer);
          for (var i = 0; i < data16Arr.length; i++) {
            nowBuffering[i] = data16Arr[i] * 0.8;
          }
        }
        var source = audioCtx.createBufferSource();
        source.buffer = myArrayBuffer;
        source.connect(audioCtx.destination);
        source.start();
        //console.log(myArrayBuffer);
      });
      //console.log(e.data)
    }

    sock.onclose = () => {
      console.log("sock close")
    }
  }
  render() {
    return (
      <div>kek</div>
    )
  }
}


export default App;
