import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { ReportComponent } from './report/report.component';
import { FeedComponent } from './feed/feed.component';
import { LoginGuardGuard } from './login-guard.guard';

//using https://angular.io/guide/router#preventing-unauthorized-access
const routes: Routes = [
  { path: '', redirectTo: 'feed', pathMatch: 'full'},
  { path: 'login', component:  LoginComponent},
  { path: 'signup', component: SignupComponent},
  { path: 'report', component:  ReportComponent,  canActivate:[LoginGuardGuard]},
  { path: 'feed', component:  FeedComponent,  canActivate:[LoginGuardGuard]},
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
