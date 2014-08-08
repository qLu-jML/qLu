#maximum angle reached by your trackIR (game value)
maxanglex = 90
maxangley = 60
# Change this if you want quicker mouse movement:
mousemultiply = 8
#how much do you lean to trigger the button (trackIR.z value)
lean = -30
lean2 = -10
#nonlinear values
mult1 = 3
end1 =  5
mult2 = 2.3
end2 = 6
mult3 = 1.8
end3 = 12
nomult = 1.1

#init
intvalue = 16384

# The non linear function :
# angle = trackIR.axis value
# maxa = trackIR axis maximum angle
# intv = intvalue
# mult = non linear multiplicator
# nlstart = until which trackIR.axis angle do the nonlinear part works
def angoutput(angle, mult, maxa):
	endangle = int(round((angle*intvalue)/maxa)*mult)
	return(endangle)

def nonlinear(angle,maxa):
	offset1 = angoutput(end1, mult1, maxa) - angoutput(end1, mult2, maxa)
	offset2 = angoutput(end1, mult1, maxa) + angoutput((end2 - end1), mult2, maxa) - angoutput(end2, mult3, maxa)
	offset3 = angoutput(end1, mult1, maxa) + angoutput((end2 - end1), mult2, maxa) + angoutput((end3 - end2), mult3, maxa) - angoutput(end3, nomult, maxa)
		
	if angle < end1 and angle > -end1:
		vjoyaxis = angoutput(angle, mult1, maxa) 

	elif angle >= end1 and angle < end2:
		vjoyaxis = angoutput(angle, mult2, maxa) + offset1

	elif angle <= -end1 and angle > -end2:
		vjoyaxis = angoutput(angle, mult2, maxa) - offset1
		
	elif angle >= end2 and angle < end3:
		vjoyaxis = angoutput(angle, mult3, maxa) + offset2

	elif angle <= -end2 and angle > -end3:
		vjoyaxis = angoutput(angle, mult3, maxa) - offset2
	
	elif angle >= end3:
		vjoyaxis = angoutput(angle, nomult, maxa) + offset3

	elif angle <= -end3:
		vjoyaxis = angoutput(angle, nomult, maxa) - offset3
		
	return(vjoyaxis)

# the code
def update():
	if (not running):
		return
	if (enabled):
		mouse.deltaX = filters.delta(trackIR.yaw)*mousemultiply
		mouse.deltaY = -(filters.delta(trackIR.pitch)*mousemultiply)
	else :
		vJoy[0].x = nonlinear(trackIR.yaw, maxanglex)
		vJoy[0].y = nonlinear(trackIR.pitch, maxangley)

	if trackIR.z > lean and trackIR.z < (lean + 10) :
		vJoy[0].setButton(2,True)
	else :	
		vJoy[0].setButton(2,False)

	if trackIR.z > lean2 and trackIR.z < (lean2 + 10) :
		vJoy[0].setButton(3,True)
	else :	
		vJoy[0].setButton(3,False)	

	

if starting:
	enabled = False
	running = True
	trackIR.update += update

toggle = joystick[2].getPressed(5)	
#toggle = joystick[0].getPressed(0)
toggle1 = joystick[0].getPressed(1)
disable = keyboard.getPressed(Key.F11)

if disable:
	running = not running 
	vJoy[0].x = 0
	vJoy[0].y = 0
	vJoy[0].z = 0

if toggle:
    enabled = not enabled
    vJoy[0].x = 0
    vJoy[0].y = 0
    vJoy[0].z = 0

#if toggle:
    #enabled = True
    
#if toggle1:
    #enabled = False
    
diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
diagnostics.watch(trackIR.yaw)
diagnostics.watch(trackIR.pitch)
diagnostics.watch(trackIR.z)
diagnostics.watch(mouse.deltaX)
diagnostics.watch(mouse.deltaY)
