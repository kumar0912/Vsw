Model Architecture Planning

Membership
      -slug  
      -type(free,pro,enterprise)
      -price
      -stripe plan id

UserMembership
      -user                     (foreignkey to default user)
      -stripe customer id
      -membership type          ( foreignkey to Membership)

Subscription
      -user Membership          (foreignkey to UserMembership)
      -stripe subscription id
      -active

Course
      -slug
      -title
      -description
      -allowed memberships         (foreignkey to membership)

Lesson
      -slug
      -title
      -Course
      -position
