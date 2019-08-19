import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Run } from '../models/run';

@Injectable({
  providedIn: 'root'
})
export class RunService {

  constructor(private http: HttpClient) { }

  public get_runs(): Observable<Run[]> {
    return this.http.get<Run[]>('/api/runs/');
  }

  public get_run(id: number): Observable<Run> {
    return this.http.get<Run>(`/api/runs/${id}/`);
  }
}
