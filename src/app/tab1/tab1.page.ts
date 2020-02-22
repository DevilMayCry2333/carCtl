import { Component } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { Vibration } from '@ionic-native/vibration/ngx';
import { HTTP } from '@ionic-native/http/ngx';
@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {
  private result = "未连接服务器";

  private downcount = 0;
  private leftcount = 0;
  private rightcount = 0;

  constructor(private alertController:AlertController,
              private vibration: Vibration,
              private http: HTTP) {

  }
  
  ionViewDidEnter(){
    console.log("view");
  }
   test(param){
     let url:string;
     if(param=="ONA"){
         url = "http://10.3.141.1:5000/up"
     }else if(param=="ONB"){
      if(this.downcount==1){
        this.downcount = 0;
        url = "http://10.3.141.1:5000/stop"
      }else{
        this.downcount += 1;
        url = "http://10.3.141.1:5000/down"
      }
     }else if(param=="ONC"){
      if(this.leftcount==1){
        this.leftcount = 0;
        url = "http://10.3.141.1:5000/stop"
      }else{
        this.leftcount += 1;
        url = "http://10.3.141.1:5000/left"
      }
     }else if(param=="OND"){
      if(this.rightcount==1){
        this.rightcount = 0;
        url = "http://10.3.141.1:5000/stop"
      }else{
        this.rightcount += 1;
        url = "http://10.3.141.1:5000/right"
      }
     }else if(param=="START"){
      url = "http://10.3.141.1:5000/start"
     }else if(param=="duoleft"){
      url = "http://10.3.141.1:5000/duoleft"
     }else if(param=="duofront"){
      url = "http://10.3.141.1:5000/duofront"
     }else if(param=="duoright"){
      url = "http://10.3.141.1:5000/duoright"
     }else if(param=="shutdown"){
      url = "http://10.3.141.1:5000/shutdown"
     }
     else{
      url = "http://10.3.141.1:5000/stop"
     }
    this.http.get(url, {}, {})
    .then(data => {
      console.log(data.status);
      console.log(data.data); // data received by server
      this.result = data.data;
      // setTimeout(()=>{
      //   this.test2();
      // },500)
      console.log(data.headers);
    })
    .catch(error => {
      console.log(error.status);
      console.log(error.error); // error message as string
      this.result = error.error;
      console.log(error.headers);
    });
    this.vibration.vibrate(1000);
  }
  test2(){
    console.log("ok2");
    this.http.get("http://10.3.141.1:5000/stop", {}, {})
    .then(data => {
      console.log(data.status);
      console.log(data.data); // data received by server
      this.result = data.data;
      console.log(data.headers);
    })
    .catch(error => {
      console.log(error.status);
      console.log(error.error); // error message as string
      this.result = error.error;
      console.log(error.headers);
    });
  }
}
