import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

/*
  Generated class for the DweetProvider provider.
  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class DweetProvider {

  private baseUrl = "https://dweet.io:443/"

  constructor(public http: Http) {
    console.log('Hello DweetProvider Provider');
  }
  //Método responsável por buscar as informações no Dweet.
  getLastestDweet(thing: string) {
    const url_get = this.baseUrl + "get/latest/dweet/for/" + thing;
    console.log(url_get);
    return this.http.get(url_get);
  }

  //Método resposnsável por modificar os dados no Dweet.
  setDweet(thing, body) {
    return this.http.post(this.baseUrl + "dweet/for/"+ thing, body);
  }

}
