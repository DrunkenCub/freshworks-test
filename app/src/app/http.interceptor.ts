import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpEvent, HttpResponse, HttpRequest, HttpHandler } from '@angular/common/http';

@Injectable()
export class HeaderInterceptor implements HttpInterceptor {

    constructor() {}

    intercept(req: HttpRequest<any>, next: HttpHandler) {
      // Get the auth token from the service.
      const authToken:any = localStorage.getItem('auth_token') || '';
  
      // Clone the request and replace the original headers with
      // cloned headers, updated with the authorization.
      const authReq = req.clone({
        headers: req.headers.set('Authorization', authToken)
      });
  
      // send cloned request with header to the next handler.
      return next.handle(authReq);
    }
}