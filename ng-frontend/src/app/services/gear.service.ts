import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Gear } from '../models/gear';

@Injectable({
  providedIn: 'root'
})
export class GearService {

  constructor(private http: HttpClient) { }

  create_gear(gear: Gear): Observable<any> {
    return this.http.post('/api/gear/', {
      name: gear.name,
      start_distance: gear.start_distance,
      start_units: gear.start_units,
      date_added: gear.date_added,
      date_retired: gear.date_retired
    });
  }

  get_gear(): Observable<Gear[]> {
    return this.http.get<Gear[]>('/api/gear/');
  }

  get(id: number): Observable<Gear> {
    return this.http.get<Gear>(`/api/gear/${id}/`);
  }

  update_gear(gear: Gear): Observable<any> {
    let pk = gear.pk;
    delete gear.pk;
    return this.http.patch(`/api/gear/${pk}/`, gear);
  }

  delete_gear(id: number): Observable<any> {
    return this.http.delete(`/api/gear/${id}/`);
  }
}
