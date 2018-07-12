import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

//É preciso importar o provideer.
import { DweetProvider } from '../../providers/dweet/dweet';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  constructor(public navCtrl: NavController, private dweetProvider: DweetProvider) {

  }

  //Declaração das Variáveis que serão usadas.
  public respostaDweet:string = "";
  public locais = new Array<any>();
  public temp = 0;
  public vol = 0;
  public sol = 0;
  public hum = 0;

  //Declaração da Model que irá ajustar o Toogle Button do Relé.
  public iluminacao_model = {
    checked: false,
    name: "iluminacao"
  }

  //Declaração da Model que irá ajustar o Toogle Button do LED.
  public irrigacao_model = {
    checked: false,
    name: "irrigacao"
  }

  ionViewDidLoad () {
    //buscando os dados no Dweet e salvando nas variáies locais
    this.dweetProvider.getLastestDweet("murilo_inatel").subscribe(
      data=>{
        const response = (data as any);
        const objeto_retorno = JSON.parse(response._body);
        this.locais = objeto_retorno.with[0].content;
        this.iluminacao_model.checked = objeto_retorno.with[0].content.iluminacao;
        this.irrigacao_model.checked = objeto_retorno.with[0].content.irrigacao;
        this.temp = objeto_retorno.with[0].content.temperatura;
        this.vol = objeto_retorno.with[0].content.volume;
        this.sol = objeto_retorno.with[0].content.sol;
        this.hum = objeto_retorno.with[0].content.humidade;

        console.log(this.locais);

      },
      error => {
        console.log(error);
      }
    )
  }

  update() {
    this.ionViewDidLoad();
  }
  //mudando o estado do LED
  change_iluminacao(){
    this.dweetPost();
    console.log(this.iluminacao_model.checked);
  }

  //Mudando o estado do Relé
  change_irrigacao(){
    this.dweetPost();
    console.log(this.irrigacao_model.checked);

  }

  dweetPost(){
    //Convertendo os dados de Boolean para Int.
    const iluminacao = ((this.iluminacao_model.checked == true) ? 1 : 0 );
    const irrigacao = ((this.irrigacao_model.checked == true) ? 1 : 0 );

    //Enviando os dados para o Dweet.io
    const json_dweet = {"iluminacao": iluminacao, "irrigacao": irrigacao, "temperatura": this.temp, "volume": this.vol, "sol": this.sol, "humidade":this.hum};
    this.dweetProvider.setDweet("murilo_inatel",json_dweet).subscribe(
      data=>{
        console.log(data);
      },
      error=> {
        console.log(error);
      }
    )
  }

}
