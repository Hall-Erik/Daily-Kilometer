import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject, of } from 'rxjs';

import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }

  logged_in = false;
  _user = new BehaviorSubject<User>(null);

  get user() { return this._user; }

  public register(): Observable<any> {
    return of(true);
  }

  public login(username: string, password: string): Observable<User> {
    this._user.next(new User({username: username, email: 'test@test.com'}));
    return this._user;
  }

  public logout(): Observable<any> {
    this._user.next(null);
    return of(true);
  }

  public get_user(): Observable<User> {
    this._user.next(new User({username: 'test', email: 'test@test.com'}));
    return this._user;
  }
}
