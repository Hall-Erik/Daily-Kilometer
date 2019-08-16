import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private USER_URL = '/api/auth/user/';
  private REGISTER_URL = '/api/auth/register/';
  private LOGIN_URL = '/api/auth/login/';
  private RESET_REQUEST_URL = '/api/auth/password/reset/';
  private VALIDATE_TOKEN_URL = '/api/auth/password/reset/validate_token/';
  private RESET_PWD_URL = '/api/password/auth/reset/confirm/';
  private CHANGE_PWD_URL = '/api/password/auth/change/';
  private LOGOUT_URL = '/api/auth/logout/';
  
  logged_in = false;
  _user = new BehaviorSubject<User>(null);
  
  get user() { return this._user; }

  constructor(private http: HttpClient) { }

  public register(username: string, email: string, password1: string, password2: string): Observable<any> {
    return this.http.post(this.REGISTER_URL, {
      username: username,
      email: email,
      password1: password1,
      password2: password2
    });
  }

  public login(username: string, password: string): Observable<any> {
    return this.http.post(this.LOGIN_URL, {
      username: username,
      password: password
    }).pipe(map(() => {
      this.get_user().subscribe();
    }));
  }

  public logout(): Observable<any> {
    this._user.next(null);
    return this.http.post(this.LOGOUT_URL, null);
  }

  public get_user(): Observable<any> {
    return this.http.get(this.USER_URL)
      .pipe(map((resp: User) => {
        this._user.next(resp);
      }));
  }

  public request_reset(email: string): Observable<any> {
    return of(true);
  }

  public validate_token(token: string): Observable<any> {
    return of(true);
  }

  public reset_password(token: string, password: string): Observable<any> {
    return of(true);
  }

  public change_password(old_password: string, new_password1: string, new_password2: string): Observable<any> {
    return of(true);
  }
}
