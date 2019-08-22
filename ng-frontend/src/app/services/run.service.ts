import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { Run } from '../models/run';

@Injectable({
  providedIn: 'root'
})
export class RunService {

  constructor(private http: HttpClient) { }
  
  public create_run(run: Run): Observable<any> {
    return this.http.post('/api/runs/', {
      run_date: run.run_date,
      distance: run.distance,
      units: run.units,
      duration: run.duration,
      gear_id: (run.gear) ? run.gear : null,
      run_type: run.run_type,
      description: run.description
    });
  }

  public get_runs(): Observable<Run[]> {
    return this.http.get<Run[]>('/api/runs/');
  }

  public get_run(id: number): Observable<Run> {
    return this.http.get<Run>(`/api/runs/${id}/`);
  }

  public delete_run(id: number): Observable<any> {
    return this.http.delete(`/api/runs/${id}/`);
  }
}
