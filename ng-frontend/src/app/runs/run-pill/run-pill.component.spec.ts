import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RunPillComponent } from './run-pill.component';

describe('RunPillComponent', () => {
  let component: RunPillComponent;
  let fixture: ComponentFixture<RunPillComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RunPillComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RunPillComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
