import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService) { }

  email!: string;
  password!: string;
  fullname!: string;
  showSpinner: boolean = false;
  admin: boolean = false;


  ngOnInit(): void {
  }

  login() : void {
    this.dataService.signup(this.email, this.password, this.fullname, this.admin).subscribe((data: any) => {
      this.router.navigate(['login'])
    }, (err)=>{
      console.log(err);
      alert(err["error"]["message"]);
    })
  }
}
