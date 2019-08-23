import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Gear } from '../models/gear';

@Injectable({
  providedIn: 'root'
})
export class GearService {

  constructor(private http: HttpClient) { }

  get_gear(): Observable<Gear[]> {
    return this.http.get<Gear[]>('/api/gear/');
  }
}
