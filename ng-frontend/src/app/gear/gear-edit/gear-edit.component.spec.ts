import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GearEditComponent } from './gear-edit.component';

describe('GearEditComponent', () => {
  let component: GearEditComponent;
  let fixture: ComponentFixture<GearEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GearEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GearEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
