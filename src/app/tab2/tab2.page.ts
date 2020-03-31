import { Component } from '@angular/core';
import { AndroidPermissions } from '@ionic-native/android-permissions/ngx';

declare var baidu_location:any;
@Component({
  selector: 'app-tab2',
  templateUrl: 'tab2.page.html',
  styleUrls: ['tab2.page.scss']
})
export class Tab2Page {

  constructor(private androidPermissions:AndroidPermissions) {

  }

  ionViewWillEnter(){
    //false;
    this.androidPermissions.checkPermission(this.androidPermissions.PERMISSION.LOCATION_HARDWARE).then(
      result => {
        console.log('Has permission?',result.hasPermission);
          this.androidPermissions.requestPermission(this.androidPermissions.PERMISSION.LOCATION_HARDWARE);
    },
      err => this.androidPermissions.requestPermission(this.androidPermissions.PERMISSION.LOCATION_HARDWARE)
    );

    baidu_location.watchPosition((data)=>{
      alert(JSON.stringify(data));
      console.log(data);
    },(msg)=>{
      alert(JSON.stringify(msg));
      console.log(msg);
    },20);

  }

}
