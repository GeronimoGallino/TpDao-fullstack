import { TestBed } from '@angular/core/testing';

import { RepFacMen } from './rep-fac-men';

describe('RepFacMen', () => {
  let service: RepFacMen;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RepFacMen);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
