program test_int
    implicit none
    
    integer :: i = 42
    complex :: z = (-3.7, 1.0)
    print *, int(i)
    print *, int(z), int(z,8)

    stop
  end program