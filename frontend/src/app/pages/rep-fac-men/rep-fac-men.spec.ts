import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RepFacMen } from './rep-fac-men';

describe('RepFacMen', () => {
  let component: RepFacMen;
  let fixture: ComponentFixture<RepFacMen>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RepFacMen]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RepFacMen);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
