import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private router: Router, private dataService: DataService) { }

  email!: string;
  password!: string;
  showSpinner: boolean = false;


  ngOnInit(): void {
  }

  login() : void {
    this.dataService.login(this.email, this.password).subscribe((data: any) => {
      localStorage.setItem('auth_token', data['auth_token']);
      this.router.navigate(['feed']);
    }, (err: any) => {
      alert("Invalid credentials");
    })
  }

  gotoSignUp() : void {
    this.router.navigate(['signup']);
  }
}