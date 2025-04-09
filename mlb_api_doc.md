Directory structure:
└── toddrob99-mlb-statsapi/
    ├── README.md
    ├── generate_endpoint_doc.py
    ├── LICENSE
    ├── requirements-dev.txt
    ├── requirements.txt
    ├── setup.py
    ├── .flake8
    ├── docs/
    │   └── index.html
    ├── statsapi/
    │   ├── __init__.py
    │   ├── endpoints.py
    │   └── version.py
    ├── tests/
    │   ├── __init__.py
    │   └── test_get.py
    └── .github/
        ├── FUNDING.yml
        └── workflows/
            └── release.yml


Files Content:

================================================
FILE: README.md
================================================
# MLB-StatsAPI

Python wrapper for MLB Stats API

Created by Todd Roberts

https://pypi.org/project/MLB-StatsAPI/

Issues: https://github.com/toddrob99/MLB-StatsAPI/issues

Wiki/Documentation: https://github.com/toddrob99/MLB-StatsAPI/wiki

## Copyright Notice

This package and its author are not affiliated with MLB or any MLB team. This API wrapper interfaces with MLB's Stats API. Use of MLB data is subject to the notice posted at http://gdx.mlb.com/components/copyright.txt.



================================================
FILE: generate_endpoint_doc.py
================================================
#!/usr/bin/env python

from statsapi import endpoints
lbb = """
* """
lb = """
"""

for k, v in endpoints.ENDPOINTS.items():
    print(f"## Endpoint: `{k}`{lb}")
    print(f"### URL: `{v['url']}`{lb}")
    rp = [pk for pk, pv in v['path_params'].items() if pv['required'] and pk != 'ver']
    # print(f"### Required Path Parameters{lb}{rp}")
    rq = [' + '.join(q) for q in v['required_params'] if len(q) > 0]
    # print(f"### Required Query Parameters{lb}{rq}")
    rp.extend(rq)
    print(f"### Required Parameters{lb}* {lbb.join(rp) if len(rp) else '*None*'}{lb}")
    ap = list(v['path_params'].keys()) + (v['query_params'] if v['query_params'] != [[]] else [])
    print(f"### All Parameters{lb}* {lbb.join(ap)}{lb}")
    if v.get("note"):
        print(f"### Note{lb}{v['note']}{lb}")

    print(f"-----{lb}")



================================================
FILE: LICENSE
================================================
                    GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

                            Preamble

  The GNU General Public License is a free, copyleft license for
software and other kinds of works.

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

  Developers that use the GNU GPL protect your rights with two steps:
(1) assert copyright on the software, and (2) offer you this License
giving you legal permission to copy, distribute and/or modify it.

  For the developers' and authors' protection, the GPL clearly explains
that there is no warranty for this free software.  For both users' and
authors' sake, the GPL requires that modified versions be marked as
changed, so that their problems will not be attributed erroneously to
authors of previous versions.

  Some devices are designed to deny users access to install or run
modified versions of the software inside them, although the manufacturer
can do so.  This is fundamentally incompatible with the aim of
protecting users' freedom to change the software.  The systematic
pattern of such abuse occurs in the area of products for individuals to
use, which is precisely where it is most unacceptable.  Therefore, we
have designed this version of the GPL to prohibit the practice for those
products.  If such problems arise substantially in other domains, we
stand ready to extend this provision to those domains in future versions
of the GPL, as needed to protect the freedom of users.

  Finally, every program is threatened constantly by software patents.
States should not allow patents to restrict development and use of
software on general-purpose computers, but in those that do, we wish to
avoid the special danger that patents applied to a free program could
make it effectively proprietary.  To prevent this, the GPL assures that
patents cannot be used to render the program non-free.

  The precise terms and conditions for copying, distribution and
modification follow.

                       TERMS AND CONDITIONS

  0. Definitions.

  "This License" refers to version 3 of the GNU General Public License.

  "Copyright" also means copyright-like laws that apply to other kinds of
works, such as semiconductor masks.

  "The Program" refers to any copyrightable work licensed under this
License.  Each licensee is addressed as "you".  "Licensees" and
"recipients" may be individuals or organizations.

  To "modify" a work means to copy from or adapt all or part of the work
in a fashion requiring copyright permission, other than the making of an
exact copy.  The resulting work is called a "modified version" of the
earlier work or a work "based on" the earlier work.

  A "covered work" means either the unmodified Program or a work based
on the Program.

  To "propagate" a work means to do anything with it that, without
permission, would make you directly or secondarily liable for
infringement under applicable copyright law, except executing it on a
computer or modifying a private copy.  Propagation includes copying,
distribution (with or without modification), making available to the
public, and in some countries other activities as well.

  To "convey" a work means any kind of propagation that enables other
parties to make or receive copies.  Mere interaction with a user through
a computer network, with no transfer of a copy, is not conveying.

  An interactive user interface displays "Appropriate Legal Notices"
to the extent that it includes a convenient and prominently visible
feature that (1) displays an appropriate copyright notice, and (2)
tells the user that there is no warranty for the work (except to the
extent that warranties are provided), that licensees may convey the
work under this License, and how to view a copy of this License.  If
the interface presents a list of user commands or options, such as a
menu, a prominent item in the list meets this criterion.

  1. Source Code.

  The "source code" for a work means the preferred form of the work
for making modifications to it.  "Object code" means any non-source
form of a work.

  A "Standard Interface" means an interface that either is an official
standard defined by a recognized standards body, or, in the case of
interfaces specified for a particular programming language, one that
is widely used among developers working in that language.

  The "System Libraries" of an executable work include anything, other
than the work as a whole, that (a) is included in the normal form of
packaging a Major Component, but which is not part of that Major
Component, and (b) serves only to enable use of the work with that
Major Component, or to implement a Standard Interface for which an
implementation is available to the public in source code form.  A
"Major Component", in this context, means a major essential component
(kernel, window system, and so on) of the specific operating system
(if any) on which the executable work runs, or a compiler used to
produce the work, or an object code interpreter used to run it.

  The "Corresponding Source" for a work in object code form means all
the source code needed to generate, install, and (for an executable
work) run the object code and to modify the work, including scripts to
control those activities.  However, it does not include the work's
System Libraries, or general-purpose tools or generally available free
programs which are used unmodified in performing those activities but
which are not part of the work.  For example, Corresponding Source
includes interface definition files associated with source files for
the work, and the source code for shared libraries and dynamically
linked subprograms that the work is specifically designed to require,
such as by intimate data communication or control flow between those
subprograms and other parts of the work.

  The Corresponding Source need not include anything that users
can regenerate automatically from other parts of the Corresponding
Source.

  The Corresponding Source for a work in source code form is that
same work.

  2. Basic Permissions.

  All rights granted under this License are granted for the term of
copyright on the Program, and are irrevocable provided the stated
conditions are met.  This License explicitly affirms your unlimited
permission to run the unmodified Program.  The output from running a
covered work is covered by this License only if the output, given its
content, constitutes a covered work.  This License acknowledges your
rights of fair use or other equivalent, as provided by copyright law.

  You may make, run and propagate covered works that you do not
convey, without conditions so long as your license otherwise remains
in force.  You may convey covered works to others for the sole purpose
of having them make modifications exclusively for you, or provide you
with facilities for running those works, provided that you comply with
the terms of this License in conveying all material for which you do
not control copyright.  Those thus making or running the covered works
for you must do so exclusively on your behalf, under your direction
and control, on terms that prohibit them from making any copies of
your copyrighted material outside their relationship with you.

  Conveying under any other circumstances is permitted solely under
the conditions stated below.  Sublicensing is not allowed; section 10
makes it unnecessary.

  3. Protecting Users' Legal Rights From Anti-Circumvention Law.

  No covered work shall be deemed part of an effective technological
measure under any applicable law fulfilling obligations under article
11 of the WIPO copyright treaty adopted on 20 December 1996, or
similar laws prohibiting or restricting circumvention of such
measures.

  When you convey a covered work, you waive any legal power to forbid
circumvention of technological measures to the extent such circumvention
is effected by exercising rights under this License with respect to
the covered work, and you disclaim any intention to limit operation or
modification of the work as a means of enforcing, against the work's
users, your or third parties' legal rights to forbid circumvention of
technological measures.

  4. Conveying Verbatim Copies.

  You may convey verbatim copies of the Program's source code as you
receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice;
keep intact all notices stating that this License and any
non-permissive terms added in accord with section 7 apply to the code;
keep intact all notices of the absence of any warranty; and give all
recipients a copy of this License along with the Program.

  You may charge any price or no price for each copy that you convey,
and you may offer support or warranty protection for a fee.

  5. Conveying Modified Source Versions.

  You may convey a work based on the Program, or the modifications to
produce it from the Program, in the form of source code under the
terms of section 4, provided that you also meet all of these conditions:

    a) The work must carry prominent notices stating that you modified
    it, and giving a relevant date.

    b) The work must carry prominent notices stating that it is
    released under this License and any conditions added under section
    7.  This requirement modifies the requirement in section 4 to
    "keep intact all notices".

    c) You must license the entire work, as a whole, under this
    License to anyone who comes into possession of a copy.  This
    License will therefore apply, along with any applicable section 7
    additional terms, to the whole of the work, and all its parts,
    regardless of how they are packaged.  This License gives no
    permission to license the work in any other way, but it does not
    invalidate such permission if you have separately received it.

    d) If the work has interactive user interfaces, each must display
    Appropriate Legal Notices; however, if the Program has interactive
    interfaces that do not display Appropriate Legal Notices, your
    work need not make them do so.

  A compilation of a covered work with other separate and independent
works, which are not by their nature extensions of the covered work,
and which are not combined with it such as to form a larger program,
in or on a volume of a storage or distribution medium, is called an
"aggregate" if the compilation and its resulting copyright are not
used to limit the access or legal rights of the compilation's users
beyond what the individual works permit.  Inclusion of a covered work
in an aggregate does not cause this License to apply to the other
parts of the aggregate.

  6. Conveying Non-Source Forms.

  You may convey a covered work in object code form under the terms
of sections 4 and 5, provided that you also convey the
machine-readable Corresponding Source under the terms of this License,
in one of these ways:

    a) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by the
    Corresponding Source fixed on a durable physical medium
    customarily used for software interchange.

    b) Convey the object code in, or embodied in, a physical product
    (including a physical distribution medium), accompanied by a
    written offer, valid for at least three years and valid for as
    long as you offer spare parts or customer support for that product
    model, to give anyone who possesses the object code either (1) a
    copy of the Corresponding Source for all the software in the
    product that is covered by this License, on a durable physical
    medium customarily used for software interchange, for a price no
    more than your reasonable cost of physically performing this
    conveying of source, or (2) access to copy the
    Corresponding Source from a network server at no charge.

    c) Convey individual copies of the object code with a copy of the
    written offer to provide the Corresponding Source.  This
    alternative is allowed only occasionally and noncommercially, and
    only if you received the object code with such an offer, in accord
    with subsection 6b.

    d) Convey the object code by offering access from a designated
    place (gratis or for a charge), and offer equivalent access to the
    Corresponding Source in the same way through the same place at no
    further charge.  You need not require recipients to copy the
    Corresponding Source along with the object code.  If the place to
    copy the object code is a network server, the Corresponding Source
    may be on a different server (operated by you or a third party)
    that supports equivalent copying facilities, provided you maintain
    clear directions next to the object code saying where to find the
    Corresponding Source.  Regardless of what server hosts the
    Corresponding Source, you remain obligated to ensure that it is
    available for as long as needed to satisfy these requirements.

    e) Convey the object code using peer-to-peer transmission, provided
    you inform other peers where the object code and Corresponding
    Source of the work are being offered to the general public at no
    charge under subsection 6d.

  A separable portion of the object code, whose source code is excluded
from the Corresponding Source as a System Library, need not be
included in conveying the object code work.

  A "User Product" is either (1) a "consumer product", which means any
tangible personal property which is normally used for personal, family,
or household purposes, or (2) anything designed or sold for incorporation
into a dwelling.  In determining whether a product is a consumer product,
doubtful cases shall be resolved in favor of coverage.  For a particular
product received by a particular user, "normally used" refers to a
typical or common use of that class of product, regardless of the status
of the particular user or of the way in which the particular user
actually uses, or expects or is expected to use, the product.  A product
is a consumer product regardless of whether the product has substantial
commercial, industrial or non-consumer uses, unless such uses represent
the only significant mode of use of the product.

  "Installation Information" for a User Product means any methods,
procedures, authorization keys, or other information required to install
and execute modified versions of a covered work in that User Product from
a modified version of its Corresponding Source.  The information must
suffice to ensure that the continued functioning of the modified object
code is in no case prevented or interfered with solely because
modification has been made.

  If you convey an object code work under this section in, or with, or
specifically for use in, a User Product, and the conveying occurs as
part of a transaction in which the right of possession and use of the
User Product is transferred to the recipient in perpetuity or for a
fixed term (regardless of how the transaction is characterized), the
Corresponding Source conveyed under this section must be accompanied
by the Installation Information.  But this requirement does not apply
if neither you nor any third party retains the ability to install
modified object code on the User Product (for example, the work has
been installed in ROM).

  The requirement to provide Installation Information does not include a
requirement to continue to provide support service, warranty, or updates
for a work that has been modified or installed by the recipient, or for
the User Product in which it has been modified or installed.  Access to a
network may be denied when the modification itself materially and
adversely affects the operation of the network or violates the rules and
protocols for communication across the network.

  Corresponding Source conveyed, and Installation Information provided,
in accord with this section must be in a format that is publicly
documented (and with an implementation available to the public in
source code form), and must require no special password or key for
unpacking, reading or copying.

  7. Additional Terms.

  "Additional permissions" are terms that supplement the terms of this
License by making exceptions from one or more of its conditions.
Additional permissions that are applicable to the entire Program shall
be treated as though they were included in this License, to the extent
that they are valid under applicable law.  If additional permissions
apply only to part of the Program, that part may be used separately
under those permissions, but the entire Program remains governed by
this License without regard to the additional permissions.

  When you convey a copy of a covered work, you may at your option
remove any additional permissions from that copy, or from any part of
it.  (Additional permissions may be written to require their own
removal in certain cases when you modify the work.)  You may place
additional permissions on material, added by you to a covered work,
for which you have or can give appropriate copyright permission.

  Notwithstanding any other provision of this License, for material you
add to a covered work, you may (if authorized by the copyright holders of
that material) supplement the terms of this License with terms:

    a) Disclaiming warranty or limiting liability differently from the
    terms of sections 15 and 16 of this License; or

    b) Requiring preservation of specified reasonable legal notices or
    author attributions in that material or in the Appropriate Legal
    Notices displayed by works containing it; or

    c) Prohibiting misrepresentation of the origin of that material, or
    requiring that modified versions of such material be marked in
    reasonable ways as different from the original version; or

    d) Limiting the use for publicity purposes of names of licensors or
    authors of the material; or

    e) Declining to grant rights under trademark law for use of some
    trade names, trademarks, or service marks; or

    f) Requiring indemnification of licensors and authors of that
    material by anyone who conveys the material (or modified versions of
    it) with contractual assumptions of liability to the recipient, for
    any liability that these contractual assumptions directly impose on
    those licensors and authors.

  All other non-permissive additional terms are considered "further
restrictions" within the meaning of section 10.  If the Program as you
received it, or any part of it, contains a notice stating that it is
governed by this License along with a term that is a further
restriction, you may remove that term.  If a license document contains
a further restriction but permits relicensing or conveying under this
License, you may add to a covered work material governed by the terms
of that license document, provided that the further restriction does
not survive such relicensing or conveying.

  If you add terms to a covered work in accord with this section, you
must place, in the relevant source files, a statement of the
additional terms that apply to those files, or a notice indicating
where to find the applicable terms.

  Additional terms, permissive or non-permissive, may be stated in the
form of a separately written license, or stated as exceptions;
the above requirements apply either way.

  8. Termination.

  You may not propagate or modify a covered work except as expressly
provided under this License.  Any attempt otherwise to propagate or
modify it is void, and will automatically terminate your rights under
this License (including any patent licenses granted under the third
paragraph of section 11).

  However, if you cease all violation of this License, then your
license from a particular copyright holder is reinstated (a)
provisionally, unless and until the copyright holder explicitly and
finally terminates your license, and (b) permanently, if the copyright
holder fails to notify you of the violation by some reasonable means
prior to 60 days after the cessation.

  Moreover, your license from a particular copyright holder is
reinstated permanently if the copyright holder notifies you of the
violation by some reasonable means, this is the first time you have
received notice of violation of this License (for any work) from that
copyright holder, and you cure the violation prior to 30 days after
your receipt of the notice.

  Termination of your rights under this section does not terminate the
licenses of parties who have received copies or rights from you under
this License.  If your rights have been terminated and not permanently
reinstated, you do not qualify to receive new licenses for the same
material under section 10.

  9. Acceptance Not Required for Having Copies.

  You are not required to accept this License in order to receive or
run a copy of the Program.  Ancillary propagation of a covered work
occurring solely as a consequence of using peer-to-peer transmission
to receive a copy likewise does not require acceptance.  However,
nothing other than this License grants you permission to propagate or
modify any covered work.  These actions infringe copyright if you do
not accept this License.  Therefore, by modifying or propagating a
covered work, you indicate your acceptance of this License to do so.

  10. Automatic Licensing of Downstream Recipients.

  Each time you convey a covered work, the recipient automatically
receives a license from the original licensors, to run, modify and
propagate that work, subject to this License.  You are not responsible
for enforcing compliance by third parties with this License.

  An "entity transaction" is a transaction transferring control of an
organization, or substantially all assets of one, or subdividing an
organization, or merging organizations.  If propagation of a covered
work results from an entity transaction, each party to that
transaction who receives a copy of the work also receives whatever
licenses to the work the party's predecessor in interest had or could
give under the previous paragraph, plus a right to possession of the
Corresponding Source of the work from the predecessor in interest, if
the predecessor has it or can get it with reasonable efforts.

  You may not impose any further restrictions on the exercise of the
rights granted or affirmed under this License.  For example, you may
not impose a license fee, royalty, or other charge for exercise of
rights granted under this License, and you may not initiate litigation
(including a cross-claim or counterclaim in a lawsuit) alleging that
any patent claim is infringed by making, using, selling, offering for
sale, or importing the Program or any portion of it.

  11. Patents.

  A "contributor" is a copyright holder who authorizes use under this
License of the Program or a work on which the Program is based.  The
work thus licensed is called the contributor's "contributor version".

  A contributor's "essential patent claims" are all patent claims
owned or controlled by the contributor, whether already acquired or
hereafter acquired, that would be infringed by some manner, permitted
by this License, of making, using, or selling its contributor version,
but do not include claims that would be infringed only as a
consequence of further modification of the contributor version.  For
purposes of this definition, "control" includes the right to grant
patent sublicenses in a manner consistent with the requirements of
this License.

  Each contributor grants you a non-exclusive, worldwide, royalty-free
patent license under the contributor's essential patent claims, to
make, use, sell, offer for sale, import and otherwise run, modify and
propagate the contents of its contributor version.

  In the following three paragraphs, a "patent license" is any express
agreement or commitment, however denominated, not to enforce a patent
(such as an express permission to practice a patent or covenant not to
sue for patent infringement).  To "grant" such a patent license to a
party means to make such an agreement or commitment not to enforce a
patent against the party.

  If you convey a covered work, knowingly relying on a patent license,
and the Corresponding Source of the work is not available for anyone
to copy, free of charge and under the terms of this License, through a
publicly available network server or other readily accessible means,
then you must either (1) cause the Corresponding Source to be so
available, or (2) arrange to deprive yourself of the benefit of the
patent license for this particular work, or (3) arrange, in a manner
consistent with the requirements of this License, to extend the patent
license to downstream recipients.  "Knowingly relying" means you have
actual knowledge that, but for the patent license, your conveying the
covered work in a country, or your recipient's use of the covered work
in a country, would infringe one or more identifiable patents in that
country that you have reason to believe are valid.

  If, pursuant to or in connection with a single transaction or
arrangement, you convey, or propagate by procuring conveyance of, a
covered work, and grant a patent license to some of the parties
receiving the covered work authorizing them to use, propagate, modify
or convey a specific copy of the covered work, then the patent license
you grant is automatically extended to all recipients of the covered
work and works based on it.

  A patent license is "discriminatory" if it does not include within
the scope of its coverage, prohibits the exercise of, or is
conditioned on the non-exercise of one or more of the rights that are
specifically granted under this License.  You may not convey a covered
work if you are a party to an arrangement with a third party that is
in the business of distributing software, under which you make payment
to the third party based on the extent of your activity of conveying
the work, and under which the third party grants, to any of the
parties who would receive the covered work from you, a discriminatory
patent license (a) in connection with copies of the covered work
conveyed by you (or copies made from those copies), or (b) primarily
for and in connection with specific products or compilations that
contain the covered work, unless you entered into that arrangement,
or that patent license was granted, prior to 28 March 2007.

  Nothing in this License shall be construed as excluding or limiting
any implied license or other defenses to infringement that may
otherwise be available to you under applicable patent law.

  12. No Surrender of Others' Freedom.

  If conditions are imposed on you (whether by court order, agreement or
otherwise) that contradict the conditions of this License, they do not
excuse you from the conditions of this License.  If you cannot convey a
covered work so as to satisfy simultaneously your obligations under this
License and any other pertinent obligations, then as a consequence you may
not convey it at all.  For example, if you agree to terms that obligate you
to collect a royalty for further conveying from those to whom you convey
the Program, the only way you could satisfy both those terms and this
License would be to refrain entirely from conveying the Program.

  13. Use with the GNU Affero General Public License.

  Notwithstanding any other provision of this License, you have
permission to link or combine any covered work with a work licensed
under version 3 of the GNU Affero General Public License into a single
combined work, and to convey the resulting work.  The terms of this
License will continue to apply to the part which is the covered work,
but the special requirements of the GNU Affero General Public License,
section 13, concerning interaction through a network will apply to the
combination as such.

  14. Revised Versions of this License.

  The Free Software Foundation may publish revised and/or new versions of
the GNU General Public License from time to time.  Such new versions will
be similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

  Each version is given a distinguishing version number.  If the
Program specifies that a certain numbered version of the GNU General
Public License "or any later version" applies to it, you have the
option of following the terms and conditions either of that numbered
version or of any later version published by the Free Software
Foundation.  If the Program does not specify a version number of the
GNU General Public License, you may choose any version ever published
by the Free Software Foundation.

  If the Program specifies that a proxy can decide which future
versions of the GNU General Public License can be used, that proxy's
public statement of acceptance of a version permanently authorizes you
to choose that version for the Program.

  Later license versions may give you additional or different
permissions.  However, no additional obligations are imposed on any
author or copyright holder as a result of your choosing to follow a
later version.

  15. Disclaimer of Warranty.

  THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

  16. Limitation of Liability.

  IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES.

  17. Interpretation of Sections 15 and 16.

  If the disclaimer of warranty and limitation of liability provided
above cannot be given local legal effect according to their terms,
reviewing courts shall apply local law that most closely approximates
an absolute waiver of all civil liability in connection with the
Program, unless a warranty or assumption of liability accompanies a
copy of the Program in return for a fee.

                     END OF TERMS AND CONDITIONS

            How to Apply These Terms to Your New Programs

  If you develop a new program, and you want it to be of the greatest
possible use to the public, the best way to achieve this is to make it
free software which everyone can redistribute and change under these terms.

  To do so, attach the following notices to the program.  It is safest
to attach them to the start of each source file to most effectively
state the exclusion of warranty; and each file should have at least
the "copyright" line and a pointer to where the full notice is found.

    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Also add information on how to contact you by electronic and paper mail.

  If the program does terminal interaction, make it output a short
notice like this when it starts in an interactive mode:

    <program>  Copyright (C) <year>  <name of author>
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.

The hypothetical commands `show w' and `show c' should show the appropriate
parts of the General Public License.  Of course, your program's commands
might be different; for a GUI interface, you would use an "about box".

  You should also get your employer (if you work as a programmer) or school,
if any, to sign a "copyright disclaimer" for the program, if necessary.
For more information on this, and how to apply and follow the GNU GPL, see
<https://www.gnu.org/licenses/>.

  The GNU General Public License does not permit incorporating your program
into proprietary programs.  If your program is a subroutine library, you
may consider it more useful to permit linking proprietary applications with
the library.  If this is what you want to do, use the GNU Lesser General
Public License instead of this License.  But first, please read
<https://www.gnu.org/licenses/why-not-lgpl.html>.



================================================
FILE: requirements-dev.txt
================================================
pytest
pytest-mock
responses



================================================
FILE: requirements.txt
================================================
requests



================================================
FILE: setup.py
================================================
import setuptools
from distutils.util import convert_path

# https://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
main_ns = {}
ver_path = convert_path("statsapi/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLB-StatsAPI",
    version=main_ns["VERSION"],
    author="Todd Roberts",
    author_email="todd@toddrob.com",
    description="MLB Stats API Wrapper for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toddrob99/MLB-StatsAPI",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)



================================================
FILE: .flake8
================================================
[flake8]
ignore = E203, E501, W503
exclude = .git,__pycache__,docs,build,dist,logs,.vscode
max-line-length = 88


================================================
FILE: docs/index.html
================================================
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="5; url=https://github.com/toddrob99/MLB-StatsAPI/wiki">
<title>MLB-StatsAPI</title>
</head>
<body>
<h2>MLB-StatsAPI</h2>
<p>Documentation has moved to <a href="https://github.com/toddrob99/MLB-StatsAPI/wiki">https://github.com/toddrob99/MLB-StatsAPI/wiki</a>.<br />You should be redirected within 5 seconds. If not, please click the link to proceed.</p>
</body>
</html>


================================================
FILE: statsapi/__init__.py
================================================
# encoding=utf-8
"""# MLB-StatsAPI

Python wrapper for MLB Stats API

Created by Todd Roberts

https://pypi.org/project/MLB-StatsAPI/

Issues: https://github.com/toddrob99/MLB-StatsAPI/issues

Wiki/Documentation: https://github.com/toddrob99/MLB-StatsAPI/wiki
"""
import sys

import copy
import logging
import requests
from datetime import datetime

from . import version
from . import endpoints

__version__ = version.VERSION
"""Installed version of MLB-StatsAPI"""

BASE_URL = endpoints.BASE_URL
"""Base MLB Stats API URL"""
ENDPOINTS = endpoints.ENDPOINTS
"""MLB Stats API endpoint configuration"""

logger = logging.getLogger("statsapi")

# Python 2 Support Warning
if sys.version_info.major < 3:
    logger.warning(
        "WARNING: Support for Python 2 has been discontinued. "
        "The MLB-StatsAPI module may continue to function, but "
        "issues not impacting Python 3 will be closed and support will not be provided."
    )


def schedule(
    date=None,
    start_date=None,
    end_date=None,
    team="",
    opponent="",
    sportId=1,
    game_id=None,
    leagueId=None,
    season=None,
    include_series_status=True,
):
    """Get list of games for a given date/range and/or team/opponent."""
    if end_date and not start_date:
        date = end_date
        end_date = None

    if start_date and not end_date:
        date = start_date
        start_date = None

    params = {}

    if date:
        params.update({"date": date})
    elif start_date and end_date:
        params.update({"startDate": start_date, "endDate": end_date})

    if team != "":
        params.update({"teamId": str(team)})

    if opponent != "":
        params.update({"opponentId": str(opponent)})

    if game_id:
        params.update({"gamePks": game_id})

    if leagueId:
        params.update({"leagueId": leagueId})

    if season:
        params.update({"season": season})

    hydrate = (
        "decisions,probablePitcher(note),linescore,broadcasts,game(content(media(epg)))"
    )
    if include_series_status:
        if date == "2014-03-11" or (str(start_date) <= "2014-03-11" <= str(end_date)):
            # For some reason the seriesStatus hydration throws a server error on 2014-03-11 only (checked back to 2000)
            logger.warning(
                "Excluding seriesStatus hydration because the MLB API throws an error for 2014-03-11 which is included in the requested date range."
            )
        else:
            hydrate += ",seriesStatus"
    params.update(
        {
            "sportId": str(sportId),
            "hydrate": hydrate,
        }
    )

    r = get("schedule", params)

    games = []
    if r.get("totalItems") == 0:
        return games  # TODO: ValueError('No games to parse from schedule object.') instead?
    else:
        for date in r.get("dates"):
            for game in date.get("games"):
                game_info = {
                    "game_id": game["gamePk"],
                    "game_datetime": game["gameDate"],
                    "game_date": date["date"],
                    "game_type": game["gameType"],
                    "status": game["status"]["detailedState"],
                    "away_name": game["teams"]["away"]["team"].get("name", "???"),
                    "home_name": game["teams"]["home"]["team"].get("name", "???"),
                    "away_id": game["teams"]["away"]["team"]["id"],
                    "home_id": game["teams"]["home"]["team"]["id"],
                    "doubleheader": game["doubleHeader"],
                    "game_num": game["gameNumber"],
                    "home_probable_pitcher": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "away_probable_pitcher": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("fullName", ""),
                    "home_pitcher_note": game["teams"]["home"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_pitcher_note": game["teams"]["away"]
                    .get("probablePitcher", {})
                    .get("note", ""),
                    "away_score": game["teams"]["away"].get("score", "0"),
                    "home_score": game["teams"]["home"].get("score", "0"),
                    "current_inning": game.get("linescore", {}).get(
                        "currentInning", ""
                    ),
                    "inning_state": game.get("linescore", {}).get("inningState", ""),
                    "venue_id": game.get("venue", {}).get("id"),
                    "venue_name": game.get("venue", {}).get("name"),
                    "national_broadcasts": list(
                        set(
                            broadcast["name"]
                            for broadcast in game.get("broadcasts", [])
                            if broadcast.get("isNational", False)
                        )
                    ),
                    "series_status": game.get("seriesStatus", {}).get("result"),
                }
                if game["content"].get("media", {}).get("freeGame", False):
                    game_info["national_broadcasts"].append("MLB.tv Free Game")
                if game_info["status"] in ["Final", "Game Over"]:
                    if game.get("isTie"):
                        game_info.update({"winning_team": "Tie", "losing_Team": "Tie"})
                    else:
                        game_info.update(
                            {
                                "winning_team": (
                                    game["teams"]["away"]["team"].get("name", "???")
                                    if game["teams"]["away"].get("isWinner")
                                    else game["teams"]["home"]["team"].get(
                                        "name", "???"
                                    )
                                ),
                                "losing_team": (
                                    game["teams"]["home"]["team"].get("name", "???")
                                    if game["teams"]["away"].get("isWinner")
                                    else game["teams"]["away"]["team"].get(
                                        "name", "???"
                                    )
                                ),
                                "winning_pitcher": game.get("decisions", {})
                                .get("winner", {})
                                .get("fullName", ""),
                                "losing_pitcher": game.get("decisions", {})
                                .get("loser", {})
                                .get("fullName", ""),
                                "save_pitcher": game.get("decisions", {})
                                .get("save", {})
                                .get("fullName"),
                            }
                        )
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"].get("name", "???")
                        + " ("
                        + str(game["teams"]["away"].get("score", ""))
                        + ") @ "
                        + game["teams"]["home"]["team"].get("name", "???")
                        + " ("
                        + str(game["teams"]["home"].get("score", ""))
                        + ") ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})
                elif game_info["status"] == "In Progress":
                    game_info.update(
                        {
                            "summary": date["date"]
                            + " - "
                            + game["teams"]["away"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["away"].get("score", "0"))
                            + ") @ "
                            + game["teams"]["home"]["team"]["name"]
                            + " ("
                            + str(game["teams"]["home"].get("score", "0"))
                            + ") ("
                            + game["linescore"]["inningState"]
                            + " of the "
                            + game["linescore"]["currentInningOrdinal"]
                            + ")"
                        }
                    )
                else:
                    summary = (
                        date["date"]
                        + " - "
                        + game["teams"]["away"]["team"]["name"]
                        + " @ "
                        + game["teams"]["home"]["team"]["name"]
                        + " ("
                        + game["status"]["detailedState"]
                        + ")"
                    )
                    game_info.update({"summary": summary})

                games.append(game_info)

        return games


def boxscore(
    gamePk,
    battingBox=True,
    battingInfo=True,
    fieldingInfo=True,
    pitchingBox=True,
    gameInfo=True,
    timecode=None,
):
    """Get a formatted boxscore for a given game."""
    boxData = boxscore_data(gamePk, timecode)

    rowLen = 79
    """rowLen is the total width of each side of the box score, excluding the " | " separator"""
    fullRowLen = rowLen * 2 + 3
    """fullRowLen is the full table width"""
    boxscore = ""
    """boxscore will hold the string to be returned"""

    if battingBox:
        # Add column headers
        awayBatters = boxData["awayBatters"]
        homeBatters = boxData["homeBatters"]

        # Make sure the home and away batter lists are the same length
        blankBatter = {
            "namefield": "",
            "ab": "",
            "r": "",
            "h": "",
            "rbi": "",
            "bb": "",
            "k": "",
            "lob": "",
            "avg": "",
            "ops": "",
        }

        while len(awayBatters) > len(homeBatters):
            homeBatters.append(blankBatter)

        while len(awayBatters) < len(homeBatters):
            awayBatters.append(blankBatter)

        # Get team totals
        awayBatters.append(boxData["awayBattingTotals"])
        homeBatters.append(boxData["homeBattingTotals"])

        # Build the batting box!
        for i in range(0, len(awayBatters)):
            if i == 0 or i == len(awayBatters) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

            boxscore += "{namefield:<40} {ab:^3} {r:^3} {h:^3} {rbi:^3} {bb:^3} {k:^3} {lob:^3} {avg:^4} {ops:^5} | ".format(
                **awayBatters[i]
            )
            boxscore += "{namefield:<40} {ab:^3} {r:^3} {h:^3} {rbi:^3} {bb:^3} {k:^3} {lob:^3} {avg:^4} {ops:^5}\n".format(
                **homeBatters[i]
            )
            if i == 0 or i == len(awayBatters) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

        # Get batting notes
        awayBattingNotes = boxData["awayBattingNotes"]
        homeBattingNotes = boxData["homeBattingNotes"]

        while len(awayBattingNotes) > len(homeBattingNotes):
            homeBattingNotes.update({len(homeBattingNotes): ""})

        while len(awayBattingNotes) < len(homeBattingNotes):
            awayBattingNotes.update({len(awayBattingNotes): ""})

        for i in range(0, len(awayBattingNotes)):
            boxscore += "{:<79} | ".format(awayBattingNotes[i])
            boxscore += "{:<79}\n".format(homeBattingNotes[i])

        boxscore += " " * rowLen + " | " + " " * rowLen + "\n"

    # Get batting and fielding info
    awayBoxInfo = {}
    homeBoxInfo = {}
    boxInfo = [awayBoxInfo, homeBoxInfo]
    sides = ["away", "home"]
    for infoType in ["BATTING", "FIELDING"]:
        if (infoType == "BATTING" and battingInfo) or (
            infoType == "FIELDING" and fieldingInfo
        ):
            for i in range(0, len(sides)):
                for z in (
                    x for x in boxData[sides[i]]["info"] if x.get("title") == infoType
                ):
                    boxInfo[i].update({len(boxInfo[i]): z["title"]})
                    for x in z["fieldList"]:
                        if len(x["label"] + ": " + x.get("value", "")) > rowLen:
                            words = iter(
                                (x["label"] + ": " + x.get("value", "")).split()
                            )
                            check = ""
                            lines = []
                            for word in words:
                                if len(check) + 1 + len(word) <= rowLen:
                                    if check == "":
                                        check = word
                                    else:
                                        check += " " + word
                                else:
                                    lines.append(check)
                                    check = "    " + word

                            if len(check):
                                lines.append(check)

                            for j in range(0, len(lines)):
                                boxInfo[i].update({len(boxInfo[i]): lines[j]})
                        else:
                            boxInfo[i].update(
                                {
                                    len(boxInfo[i]): x["label"]
                                    + ": "
                                    + x.get("value", "")
                                }
                            )

            if infoType == "BATTING":
                if len(awayBoxInfo):
                    awayBoxInfo.update({len(awayBoxInfo): " "})

                if len(homeBoxInfo):
                    homeBoxInfo.update({len(homeBoxInfo): " "})

    if len(awayBoxInfo) > 0:
        while len(awayBoxInfo) > len(homeBoxInfo):
            homeBoxInfo.update({len(homeBoxInfo): ""})

        while len(awayBoxInfo) < len(homeBoxInfo):
            awayBoxInfo.update({len(awayBoxInfo): ""})

        # Build info box
        for i in range(0, len(awayBoxInfo)):
            boxscore += ("{:<%s} | " % rowLen).format(awayBoxInfo[i])
            boxscore += ("{:<%s}\n" % rowLen).format(homeBoxInfo[i])
            if i == len(awayBoxInfo) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

    # Get pitching box
    if pitchingBox:
        awayPitchers = boxData["awayPitchers"]
        homePitchers = boxData["homePitchers"]

        # Make sure the home and away pitcher lists are the same length
        blankPitcher = {
            "namefield": "",
            "ip": "",
            "h": "",
            "r": "",
            "er": "",
            "bb": "",
            "k": "",
            "hr": "",
            "era": "",
        }

        while len(awayPitchers) > len(homePitchers):
            homePitchers.append(blankPitcher)

        while len(awayPitchers) < len(homePitchers):
            awayPitchers.append(blankPitcher)

        # Get team totals
        awayPitchers.append(boxData["awayPitchingTotals"])
        homePitchers.append(boxData["homePitchingTotals"])

        # Build the pitching box!
        for i in range(0, len(awayPitchers)):
            if i == 0 or i == len(awayPitchers) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

            boxscore += "{namefield:<43} {ip:^4} {h:^3} {r:^3} {er:^3} {bb:^3} {k:^3} {hr:^3} {era:^6} | ".format(
                **awayPitchers[i]
            )
            boxscore += "{namefield:<43} {ip:^4} {h:^3} {r:^3} {er:^3} {bb:^3} {k:^3} {hr:^3} {era:^6}\n".format(
                **homePitchers[i]
            )
            if i == 0 or i == len(awayPitchers) - 1:
                boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

    # Get game info
    if gameInfo:
        z = boxData["gameBoxInfo"]
        gameBoxInfo = {}
        for x in z:
            if (
                len(x["label"] + (": " if x.get("value") else "") + x.get("value", ""))
                > fullRowLen
            ):
                words = iter(
                    (
                        x["label"]
                        + (": " if x.get("value") else "")
                        + x.get("value", "")
                    ).split()
                )
                check = ""
                lines = []
                for word in words:
                    if len(check) + 1 + len(word) <= fullRowLen:
                        if check == "":
                            check = word
                        else:
                            check += " " + word
                    else:
                        lines.append(check)
                        check = "    " + word

                if len(check):
                    lines.append(check)

                for i in range(0, len(lines)):
                    gameBoxInfo.update({len(gameBoxInfo): lines[i]})
            else:
                gameBoxInfo.update(
                    {
                        len(gameBoxInfo): x["label"]
                        + (": " if x.get("value") else "")
                        + x.get("value", "")
                    }
                )

        # Build the game info box
        for i in range(0, len(gameBoxInfo)):
            boxscore += ("{:<%s}" % fullRowLen + "\n").format(gameBoxInfo[i])
            if i == len(gameBoxInfo) - 1:
                boxscore += "-" * fullRowLen + "\n"

    return boxscore


def boxscore_data(gamePk, timecode=None):
    """Returns a python dict containing boxscore data for a given game."""

    boxData = {}
    """boxData holds the dict to be returned"""

    params = {
        "gamePk": gamePk,
        "fields": "gameData,game,teams,teamName,shortName,teamStats,batting,atBats,runs,hits,doubles,triples,homeRuns,rbi,stolenBases,strikeOuts,baseOnBalls,leftOnBase,pitching,inningsPitched,earnedRuns,homeRuns,players,boxscoreName,liveData,boxscore,teams,players,id,fullName,allPositions,abbreviation,seasonStats,batting,avg,ops,obp,slg,era,pitchesThrown,numberOfPitches,strikes,battingOrder,info,title,fieldList,note,label,value,wins,losses,holds,blownSaves",
    }
    if timecode:
        params.update({"timecode": timecode})

    r = get("game", params)

    boxData.update({"gameId": r["gameData"]["game"]["id"]})
    boxData.update({"teamInfo": r["gameData"]["teams"]})
    boxData.update({"playerInfo": r["gameData"]["players"]})
    boxData.update({"away": r["liveData"]["boxscore"]["teams"]["away"]})
    boxData.update({"home": r["liveData"]["boxscore"]["teams"]["home"]})

    batterColumns = [
        {
            "namefield": boxData["teamInfo"]["away"]["teamName"] + " Batters",
            "ab": "AB",
            "r": "R",
            "h": "H",
            "doubles": "2B",
            "triples": "3B",
            "hr": "HR",
            "rbi": "RBI",
            "sb": "SB",
            "bb": "BB",
            "k": "K",
            "lob": "LOB",
            "avg": "AVG",
            "ops": "OPS",
            "personId": 0,
            "substitution": False,
            "note": "",
            "name": boxData["teamInfo"]["away"]["teamName"] + " Batters",
            "position": "",
            "obp": "OBP",
            "slg": "SLG",
            "battingOrder": "",
        }
    ]
    # Add away and home column headers
    sides = ["away", "home"]
    awayBatters = copy.deepcopy(batterColumns)
    homeBatters = copy.deepcopy(batterColumns)
    homeBatters[0]["namefield"] = boxData["teamInfo"]["home"]["teamName"] + " Batters"
    homeBatters[0]["name"] = boxData["teamInfo"]["home"]["teamName"] + " Batters"
    batters = [awayBatters, homeBatters]

    for i in range(0, len(sides)):
        side = sides[i]
        for batterId_int in [
            x
            for x in boxData[side]["batters"]
            if boxData[side]["players"].get("ID" + str(x), {}).get("battingOrder")
        ]:
            batterId = str(batterId_int)
            namefield = (
                str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[0]
                if str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[-1]
                == "0"
                else "   "
            )
            namefield += " " + boxData[side]["players"]["ID" + batterId]["stats"][
                "batting"
            ].get("note", "")
            namefield += (
                boxData["playerInfo"]["ID" + batterId]["boxscoreName"]
                + "  "
                + boxData[side]["players"]["ID" + batterId]["position"]["abbreviation"]
            )
            if not len(
                boxData[side]["players"]["ID" + batterId]
                .get("stats", {})
                .get("batting", {})
            ):
                # Protect against player with no batting data in the box score (#37)
                continue

            batter = {
                "namefield": namefield,
                "ab": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "atBats"
                    ]
                ),
                "r": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "runs"
                    ]
                ),
                "h": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "hits"
                    ]
                ),
                "doubles": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "doubles"
                    ]
                ),
                "triples": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "triples"
                    ]
                ),
                "hr": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "homeRuns"
                    ]
                ),
                "rbi": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"]["rbi"]
                ),
                "sb": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "stolenBases"
                    ]
                ),
                "bb": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "baseOnBalls"
                    ]
                ),
                "k": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "strikeOuts"
                    ]
                ),
                "lob": str(
                    boxData[side]["players"]["ID" + batterId]["stats"]["batting"][
                        "leftOnBase"
                    ]
                ),
                "avg": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "avg"
                    ]
                ),
                "ops": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "ops"
                    ]
                ),
                "personId": batterId_int,
                "battingOrder": str(
                    boxData[side]["players"]["ID" + batterId]["battingOrder"]
                ),
                "substitution": (
                    False
                    if str(boxData[side]["players"]["ID" + batterId]["battingOrder"])[
                        -1
                    ]
                    == "0"
                    else True
                ),
                "note": boxData[side]["players"]["ID" + batterId]["stats"][
                    "batting"
                ].get("note", ""),
                "name": boxData["playerInfo"]["ID" + batterId]["boxscoreName"],
                "position": boxData[side]["players"]["ID" + batterId]["position"][
                    "abbreviation"
                ],
                "obp": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "obp"
                    ]
                ),
                "slg": str(
                    boxData[side]["players"]["ID" + batterId]["seasonStats"]["batting"][
                        "slg"
                    ]
                ),
            }
            batters[i].append(batter)

    boxData.update({"awayBatters": awayBatters})
    boxData.update({"homeBatters": homeBatters})

    # Add team totals
    sidesBattingTotals = ["awayBattingTotals", "homeBattingTotals"]
    for i in range(0, len(sides)):
        side = sides[i]
        boxData.update(
            {
                sidesBattingTotals[i]: {
                    "namefield": "Totals",
                    "ab": str(boxData[side]["teamStats"]["batting"]["atBats"]),
                    "r": str(boxData[side]["teamStats"]["batting"]["runs"]),
                    "h": str(boxData[side]["teamStats"]["batting"]["hits"]),
                    "hr": str(boxData[side]["teamStats"]["batting"]["homeRuns"]),
                    "rbi": str(boxData[side]["teamStats"]["batting"]["rbi"]),
                    "bb": str(boxData[side]["teamStats"]["batting"]["baseOnBalls"]),
                    "k": str(boxData[side]["teamStats"]["batting"]["strikeOuts"]),
                    "lob": str(boxData[side]["teamStats"]["batting"]["leftOnBase"]),
                    "avg": "",
                    "ops": "",
                    "obp": "",
                    "slg": "",
                    "name": "Totals",
                    "position": "",
                    "note": "",
                    "substitution": False,
                    "battingOrder": "",
                    "personId": 0,
                }
            }
        )

    # Get batting notes
    awayBattingNotes = {}
    homeBattingNotes = {}
    battingNotes = [awayBattingNotes, homeBattingNotes]
    for i in range(0, len(sides)):
        for n in boxData[sides[i]]["note"]:
            battingNotes[i].update(
                {len(battingNotes[i]): n["label"] + "-" + n["value"]}
            )

    boxData.update({"awayBattingNotes": awayBattingNotes})
    boxData.update({"homeBattingNotes": homeBattingNotes})

    # Get pitching box
    # Add column headers
    pitcherColumns = [
        {
            "namefield": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
            "ip": "IP",
            "h": "H",
            "r": "R",
            "er": "ER",
            "bb": "BB",
            "k": "K",
            "hr": "HR",
            "era": "ERA",
            "p": "P",
            "s": "S",
            "name": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
            "personId": 0,
            "note": "",
        }
    ]
    awayPitchers = copy.deepcopy(pitcherColumns)
    homePitchers = copy.deepcopy(pitcherColumns)
    homePitchers[0]["namefield"] = boxData["teamInfo"]["home"]["teamName"] + " Pitchers"
    homePitchers[0]["name"] = boxData["teamInfo"]["away"]["teamName"] + " Pitchers"
    pitchers = [awayPitchers, homePitchers]

    for i in range(0, len(sides)):
        side = sides[i]
        for pitcherId_int in boxData[side]["pitchers"]:
            pitcherId = str(pitcherId_int)
            if not boxData[side]["players"].get("ID" + pitcherId) or not len(
                boxData[side]["players"]["ID" + pitcherId]
                .get("stats", {})
                .get("pitching", {})
            ):
                # Skip pitcher with no pitching data in the box score (#37)
                # Or skip pitcher listed under the wrong team (from comments on #37)
                continue

            namefield = boxData["playerInfo"]["ID" + pitcherId]["boxscoreName"]
            namefield += (
                "  "
                + boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                    "note", ""
                )
                if boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                    "note"
                )
                else ""
            )
            pitcher = {
                "namefield": namefield,
                "ip": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "inningsPitched"
                    ]
                ),
                "h": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "hits"
                    ]
                ),
                "r": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "runs"
                    ]
                ),
                "er": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "earnedRuns"
                    ]
                ),
                "bb": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "baseOnBalls"
                    ]
                ),
                "k": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "strikeOuts"
                    ]
                ),
                "hr": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "homeRuns"
                    ]
                ),
                "p": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"].get(
                        "pitchesThrown",
                        boxData[side]["players"]["ID" + pitcherId]["stats"][
                            "pitching"
                        ].get("numberOfPitches", 0),
                    )
                ),
                "s": str(
                    boxData[side]["players"]["ID" + pitcherId]["stats"]["pitching"][
                        "strikes"
                    ]
                ),
                "era": str(
                    boxData[side]["players"]["ID" + pitcherId]["seasonStats"][
                        "pitching"
                    ]["era"]
                ),
                "name": boxData["playerInfo"]["ID" + pitcherId]["boxscoreName"],
                "personId": pitcherId_int,
                "note": boxData[side]["players"]["ID" + pitcherId]["stats"][
                    "pitching"
                ].get("note", ""),
            }
            pitchers[i].append(pitcher)

    boxData.update({"awayPitchers": awayPitchers})
    boxData.update({"homePitchers": homePitchers})

    # Get team totals
    pitchingTotals = ["awayPitchingTotals", "homePitchingTotals"]
    for i in range(0, len(sides)):
        side = sides[i]
        boxData.update(
            {
                pitchingTotals[i]: {
                    "namefield": "Totals",
                    "ip": str(boxData[side]["teamStats"]["pitching"]["inningsPitched"]),
                    "h": str(boxData[side]["teamStats"]["pitching"]["hits"]),
                    "r": str(boxData[side]["teamStats"]["pitching"]["runs"]),
                    "er": str(boxData[side]["teamStats"]["pitching"]["earnedRuns"]),
                    "bb": str(boxData[side]["teamStats"]["pitching"]["baseOnBalls"]),
                    "k": str(boxData[side]["teamStats"]["pitching"]["strikeOuts"]),
                    "hr": str(boxData[side]["teamStats"]["pitching"]["homeRuns"]),
                    "p": "",
                    "s": "",
                    "era": "",
                    "name": "Totals",
                    "personId": 0,
                    "note": "",
                }
            }
        )

    # Get game info
    boxData.update({"gameBoxInfo": r["liveData"]["boxscore"].get("info", [])})

    return boxData


def linescore(gamePk, timecode=None):
    """Get formatted linescore for a given game."""
    linescore = ""
    params = {
        "gamePk": gamePk,
        "fields": "gameData,teams,teamName,shortName,status,abstractGameState,liveData,linescore,innings,num,home,away,runs,hits,errors",
    }
    if timecode:
        params.update({"timecode": timecode})

    r = get("game", params)

    header_name = r["gameData"]["status"]["abstractGameState"]
    away_name = r["gameData"]["teams"]["away"]["teamName"]
    home_name = r["gameData"]["teams"]["home"]["teamName"]
    header_row = []
    away = []
    home = []

    for x in r["liveData"]["linescore"]["innings"]:
        header_row.append(str(x.get("num", "")))
        away.append(str(x.get("away", {}).get("runs", 0)))
        home.append(str(x.get("home", {}).get("runs", 0)))

    if len(r["liveData"]["linescore"]["innings"]) < 9:
        for i in range(len(r["liveData"]["linescore"]["innings"]) + 1, 10):
            header_row.append(str(i))
            away.append(" ")
            home.append(" ")

    header_row.extend(["R", "H", "E"])
    away_prefix = r["liveData"]["linescore"].get("teams", {}).get("away", {})
    away.extend(
        [
            str(away_prefix.get("runs", 0)),
            str(away_prefix.get("hits", 0)),
            str(away_prefix.get("errors", 0)),
        ]
    )
    home_prefix = r["liveData"]["linescore"].get("teams", {}).get("home", {})
    home.extend(
        [
            str(home_prefix.get("runs", 0)),
            str(home_prefix.get("hits", 0)),
            str(home_prefix.get("errors", 0)),
        ]
    )

    # Build the linescore
    for k in [[header_name, header_row], [away_name, away], [home_name, home]]:
        linescore += (
            "{:<%s}" % str(len(max([header_name, away_name, home_name], key=len)) + 1)
        ).format(k[0])
        linescore += ("{:^2}" * (len(k[1]) - 3)).format(*k[1])
        linescore += ("{:^4}" * 3).format(*k[1][-3:])
        linescore += "\n"

    if len(linescore) > 1:
        linescore = linescore[:-1]  # strip the extra line break

    return linescore


def last_game(teamId):
    """Get the gamePk for the given team's most recent completed game."""
    previousSchedule = get(
        "team",
        {
            "teamId": teamId,
            "hydrate": "previousSchedule",
            "fields": "teams,team,id,previousGameSchedule,dates,date,games,gamePk,gameDate,status,abstractGameCode",
        },
    )
    games = []
    for d in previousSchedule["teams"][0]["previousGameSchedule"]["dates"]:
        games.extend([x for x in d["games"] if x["status"]["abstractGameCode"] == "F"])

    if not len(games):
        return None

    return games[-1]["gamePk"]


def next_game(teamId):
    """Get the gamePk for the given team's next unstarted game."""
    nextSchedule = get(
        "team",
        {
            "teamId": teamId,
            "hydrate": "nextSchedule",
            "fields": "teams,team,id,nextGameSchedule,dates,date,games,gamePk,gameDate,status,abstractGameCode",
        },
    )
    games = []
    for d in nextSchedule["teams"][0]["nextGameSchedule"]["dates"]:
        games.extend([x for x in d["games"] if x["status"]["abstractGameCode"] == "P"])

    if not len(games):
        return None

    return games[0]["gamePk"]


def game_scoring_plays(gamePk):
    """Get a text-formatted list of scoring plays for a given game."""
    sortedPlays = game_scoring_play_data(gamePk)
    scoring_plays = ""
    for a in sortedPlays["plays"]:
        scoring_plays += "{}\n{} {} - {}: {}, {}: {}\n\n".format(
            a["result"]["description"],
            a["about"]["halfInning"][0:1].upper() + a["about"]["halfInning"][1:],
            a["about"]["inning"],
            sortedPlays["away"]["name"],
            a["result"]["awayScore"],
            sortedPlays["home"]["name"],
            a["result"]["homeScore"],
        )

    if len(scoring_plays) > 1:
        scoring_plays = scoring_plays[:-2]  # strip the extra line break

    return scoring_plays


def game_scoring_play_data(gamePk):
    """Returns a python dict of scoring plays for a given game containing 3 keys:

    * home - home team data
    * away - away team data
    * plays - sorted list of scoring play data
    """
    r = get(
        "game",
        {
            "gamePk": gamePk,
            "fields": (
                "gamePk,link,gameData,game,pk,teams,away,id,name,teamCode,fileCode,"
                "abbreviation,teamName,locationName,shortName,home,liveData,plays,"
                "allPlays,scoringPlays,scoringPlays,atBatIndex,result,description,"
                "awayScore,homeScore,about,halfInning,inning,endTime"
            ),
        },
    )
    if not len(r["liveData"]["plays"].get("scoringPlays", [])):
        return {
            "home": r["gameData"]["teams"]["home"],
            "away": r["gameData"]["teams"]["away"],
            "plays": [],
        }

    unorderedPlays = {}
    for i in r["liveData"]["plays"].get("scoringPlays", []):
        play = next(
            (p for p in r["liveData"]["plays"]["allPlays"] if p.get("atBatIndex") == i),
            None,
        )
        if play:
            unorderedPlays.update({play["about"]["endTime"]: play})

    sortedPlays = []
    for x in sorted(unorderedPlays):
        sortedPlays.append(unorderedPlays[x])

    return {
        "home": r["gameData"]["teams"]["home"],
        "away": r["gameData"]["teams"]["away"],
        "plays": sortedPlays,
    }


def game_highlights(gamePk):
    """Get the highlight video links for a given game."""
    sortedHighlights = game_highlight_data(gamePk)

    highlights = ""
    for a in sortedHighlights:
        # if sum(1 for t in a['keywordsAll'] if t['type']=='team_id') == 1:
        #    highlights += next(t['displayName'] for t in a['keywordsAll'] if t['type']=='team_id') + '\n'
        highlights += "{} ({})\n{}\n{}\n\n".format(
            a.get("title", a.get("headline", "")),
            a["duration"],
            a.get("description", ""),
            next(
                (s["url"] for s in a["playbacks"] if s["name"] == "mp4Avc"),
                next(
                    (
                        s["url"]
                        for s in a["playbacks"]
                        if s["name"] == "FLASH_2500K_1280X720"
                    ),
                    "Link not found",
                ),
            ),
        )

    return highlights


def game_highlight_data(gamePk):
    """Returns a list of highlight data for a given game."""
    r = get(
        "schedule",
        {
            "sportId": 1,
            "gamePk": gamePk,
            "hydrate": "game(content(highlights(highlights)))",
            "fields": "dates,date,games,gamePk,content,highlights,items,headline,type,value,title,description,duration,playbacks,name,url",
        },
    )
    gameHighlights = (
        r["dates"][0]["games"][0]
        .get("content", {})
        .get("highlights", {})
        .get("highlights", {})
    )
    if not gameHighlights or not len(gameHighlights.get("items", [])):
        return []

    unorderedHighlights = {}
    for v in (
        x
        for x in gameHighlights["items"]
        if isinstance(x, dict) and x["type"] == "video"
    ):
        unorderedHighlights.update({v["date"]: v})

    sortedHighlights = []
    for x in sorted(unorderedHighlights):
        sortedHighlights.append(unorderedHighlights[x])

    return sortedHighlights


def game_pace(season=datetime.now().year, sportId=1):
    """Get a text-formatted list about pace of game for a given season (back to 1999)."""
    r = game_pace_data(season, sportId)

    pace = ""

    pace += "{} Game Pace Stats\n".format(season)
    for s in r["sports"]:
        for k in s.keys():
            if k in ["season", "sport"]:
                continue

            if k == "prPortalCalculatedFields":
                for x in s[k].keys():
                    pace += "{}: {}\n".format(x, s[k][x])
            else:
                pace += "{}: {}\n".format(k, s[k])

    return pace


def game_pace_data(season=datetime.now().year, sportId=1):
    """Returns data about pace of game for a given season (back to 1999)."""
    params = {}
    if season:
        params.update({"season": season})

    if sportId:
        params.update({"sportId": sportId})

    r = get("gamePace", params)

    if not len(r["sports"]):
        raise ValueError(
            "No game pace info found for the {} season. Game pace data appears to begin in 1999.".format(
                season
            )
        )

    return r


def player_stats(
    personId, group="[hitting,pitching,fielding]", type="season", season=None
):
    """Get current season or career stats for a given player."""
    player = player_stat_data(personId, group, type, season)

    stats = ""
    stats += player["first_name"]
    if player["nickname"]:
        stats += ' "{nickname}"'.format(**player)

    stats += " {last_name}, {position} ({mlb_debut:.4}-".format(**player)
    if not player["active"]:
        stats += "{last_played:.4}".format(**player)

    stats += ")\n\n"

    for x in player["stats"]:
        stats += (
            x["type"][0:1].upper()
            + x["type"][1:]
            + " "
            + x["group"][0:1].upper()
            + x["group"][1:]
        )
        if x["stats"].get("position"):
            stats += " ({})".format(x["stats"]["position"]["abbreviation"])

        stats += "\n"
        for y in x["stats"].keys():
            if y == "position":
                continue
            stats += "{}: {}\n".format(y, x["stats"][y])

        stats += "\n"

    return stats


def player_stat_data(
    personId, group="[hitting,pitching,fielding]", type="season", sportId=1, season=None
):
    """Returns a list of current season or career stat data for a given player."""

    if season is not None and "season" not in type:
        raise ValueError(
            "The 'season' parameter is only valid when using the 'season' type."
        )

    params = {
        "personId": personId,
        "hydrate": "stats(group="
        + group
        + ",type="
        + type
        + (",season=" + str(season) if season else "")
        + ",sportId="
        + str(sportId)
        + "),currentTeam",
    }
    r = get("person", params)

    stat_groups = []

    player = {
        "id": r["people"][0]["id"],
        "first_name": r["people"][0]["useName"],
        "last_name": r["people"][0]["lastName"],
        "active": r["people"][0]["active"],
        "current_team": r["people"][0]["currentTeam"]["name"],
        "position": r["people"][0]["primaryPosition"]["abbreviation"],
        "nickname": r["people"][0].get("nickName"),
        "last_played": r["people"][0].get("lastPlayedDate"),
        "mlb_debut": r["people"][0].get("mlbDebutDate"),
        "bat_side": r["people"][0]["batSide"]["description"],
        "pitch_hand": r["people"][0]["pitchHand"]["description"],
    }

    for s in r["people"][0].get("stats", []):
        for i in range(0, len(s["splits"])):
            stat_group = {
                "type": s["type"]["displayName"],
                "group": s["group"]["displayName"],
                "season": s["splits"][i].get("season"),
                "stats": s["splits"][i]["stat"],
            }
            stat_groups.append(stat_group)

    player.update({"stats": stat_groups})

    return player


def latest_season(sportId=1):
    """Get the latest season for a given sportId. Returns a dict containing seasonId and various dates."""
    params = {
        "sportId": sportId,
        "seasonId": "all",
    }
    all_seasons = get("season", params)
    return next(
        (
            s
            for s in all_seasons.get("seasons", [])
            if (datetime.today().strftime("%Y-%m-%d") < s.get("seasonEndDate", ""))
        ),
        all_seasons["seasons"][-1],
    )


def lookup_player(lookup_value, gameType=None, season=None, sportId=1):
    """Get data about players based on first, last, or full name."""
    params = {
        "sportId": sportId,
        "fields": "people,id,fullName,firstName,lastName,primaryNumber,currentTeam,id,primaryPosition,code,abbreviation,useName,boxscoreName,nickName,mlbDebutDate,nameFirstLast,firstLastName,lastFirstName,lastInitName,initLastName,fullFMLName,fullLFMName,nameSlug",
    }
    if gameType:
        params.update(
            {
                "gameType": gameType,
            }
        )
    if not season:
        season_data = latest_season(sportId=sportId)
        season = season_data.get("seasonId", datetime.now().year)
    params.update(
        {
            "season": season,
        }
    )
    r = get("sports_players", params)

    players = []
    lookup_values = str(lookup_value).lower().split()
    for player in r["people"]:
        for l in lookup_values:
            for v in player.values():
                if l in str(v).lower():
                    break
            else:
                break
        else:
            players.append(player)

    return players


def lookup_team(lookup_value, activeStatus="Y", season=None, sportIds=1):
    """Get a info about a team or teams based on the team name, city, abbreviation, or file code."""
    params = {
        "activeStatus": activeStatus,
        "sportIds": sportIds,
        "fields": "teams,id,name,teamCode,fileCode,teamName,locationName,shortName",
    }
    if not season:
        season_data = latest_season(sportId=str(sportIds).split(",")[0])
        season = season_data.get("seasonId", datetime.now().year)
    params.update(
        {
            "season": season,
        }
    )
    r = get("teams", params)

    teams = []
    for team in r["teams"]:
        for v in team.values():
            if str(lookup_value).lower() in str(v).lower():
                teams.append(team)
                break

    return teams


def team_leaders(
    teamId, leaderCategories, season=datetime.now().year, leaderGameTypes="R", limit=10
):
    """Get stat leaders for a given team."""
    lines = team_leader_data(teamId, leaderCategories, season, leaderGameTypes, limit)

    leaders = ""

    leaders += "{:<4} {:<20} {:<5}\n".format(*["Rank", "Name", "Value"])
    for a in lines:
        leaders += "{:^4} {:<20} {:^5}\n".format(*a)

    return leaders


def team_leader_data(
    teamId, leaderCategories, season=datetime.now().year, leaderGameTypes="R", limit=10
):
    """Returns a python list of stat leader data for a given team."""
    params = {
        "leaderCategories": leaderCategories,
        "season": season,
        "teamId": teamId,
        "leaderGameTypes": leaderGameTypes,
        "limit": limit,
    }
    params.update({"fields": "teamLeaders,leaders,rank,value,person,fullName"})

    r = get("team_leaders", params)

    lines = []
    for player in [x for x in r["teamLeaders"][0]["leaders"]]:
        lines.append([player["rank"], player["person"]["fullName"], player["value"]])

    return lines


def league_leaders(
    leaderCategories,
    season=None,
    limit=10,
    statGroup=None,
    leagueId=None,
    gameTypes=None,
    playerPool=None,
    sportId=1,
    statType=None,
):
    """Get stat leaders overall or for a given league (103=AL, 104=NL)."""
    lines = league_leader_data(
        leaderCategories,
        season,
        limit,
        statGroup,
        leagueId,
        gameTypes,
        playerPool,
        sportId,
        statType,
    )

    leaders = ""

    leaders += "{:<4} {:<20} {:<23} {:<5}\n".format(*["Rank", "Name", "Team", "Value"])
    for a in lines:
        leaders += "{:^4} {:<20} {:<23} {:^5}\n".format(*a)

    return leaders


def league_leader_data(
    leaderCategories,
    season=None,
    limit=10,
    statGroup=None,
    leagueId=None,
    gameTypes=None,
    playerPool=None,
    sportId=1,
    statType=None,
):
    """Returns a python list of stat leaders overall or for a given league (103=AL, 104=NL)."""
    params = {"leaderCategories": leaderCategories, "sportId": sportId, "limit": limit}
    if season:
        params.update({"season": season})

    if statType:
        params.update({"statType": statType})

    if not season and not statType:
        params.update(
            {"season": datetime.now().year}
        )  # default season to current year if no season or statType provided

    if statGroup:
        if statGroup == "batting":
            statGroup = "hitting"

        params.update({"statGroup": statGroup})

    if gameTypes:
        params.update({"leaderGameTypes": gameTypes})

    if leagueId:
        params.update({"leagueId": leagueId})

    if playerPool:
        params.update({"playerPool": playerPool})

    params.update(
        {
            "fields": "leagueLeaders,leaders,rank,value,team,name,league,name,person,fullName"
        }
    )

    r = get("stats_leaders", params)

    lines = []
    for player in [x for x in r["leagueLeaders"][0]["leaders"]]:
        lines.append(
            [
                player["rank"],
                player["person"]["fullName"],
                player["team"].get("name", ""),
                player["value"],
            ]
        )

    return lines


def standings(
    leagueId="103,104",
    division="all",
    include_wildcard=True,
    season=None,
    standingsTypes=None,
    date=None,
):
    """Get formatted standings for a given league/division and season."""
    divisions = standings_data(
        leagueId, division, include_wildcard, season, standingsTypes, date
    )

    standings = ""

    for div in divisions.values():
        standings += div["div_name"] + "\n"
        if include_wildcard:
            standings += (
                "{:^4} {:<21} {:^3} {:^3} {:^4} {:^4} {:^7} {:^5} {:^4}\n".format(
                    *[
                        "Rank",
                        "Team",
                        "W",
                        "L",
                        "GB",
                        "(E#)",
                        "WC Rank",
                        "WC GB",
                        "(E#)",
                    ]
                )
            )
            for t in div["teams"]:
                standings += "{div_rank:^4} {name:<21} {w:^3} {l:^3} {gb:^4} {elim_num:^4} {wc_rank:^7} {wc_gb:^5} {wc_elim_num:^4}\n".format(
                    **t
                )
        else:
            standings += "{:^4} {:<21} {:^3} {:^3} {:^4} {:^4}\n".format(
                *["Rank", "Team", "W", "L", "GB", "(E#)"]
            )
            for t in div["teams"]:
                standings += "{div_rank:^4} {name:<21} {w:^3} {l:^3} {gb:^4} {elim_num:^4}\n".format(
                    **t
                )
        standings += "\n"

    return standings


def standings_data(
    leagueId="103,104",
    division="all",
    include_wildcard=True,
    season=None,
    standingsTypes=None,
    date=None,
):
    """Returns a dict of standings data for a given league/division and season."""
    params = {"leagueId": leagueId}
    if date:
        params.update({"date": date})

    if not season:
        if date:
            season = date[-4:]
        else:
            season = datetime.now().year

    if not standingsTypes:
        standingsTypes = "regularSeason"

    params.update({"season": season, "standingsTypes": standingsTypes})
    params.update(
        {
            "hydrate": "team(division)",
            "fields": "records,standingsType,teamRecords,team,name,division,id,nameShort,abbreviation,divisionRank,gamesBack,wildCardRank,wildCardGamesBack,wildCardEliminationNumber,divisionGamesBack,clinched,eliminationNumber,winningPercentage,type,wins,losses,leagueRank,sportRank",
        }
    )

    r = get("standings", params)

    divisions = {}

    for y in r["records"]:
        for x in (
            x
            for x in y["teamRecords"]
            if str(division).lower() == "all"
            or str(division).lower() == x["team"]["division"]["abbreviation"].lower()
            or str(division) == str(x["team"]["division"]["id"])
        ):
            if x["team"]["division"]["id"] not in divisions.keys():
                divisions.update(
                    {
                        x["team"]["division"]["id"]: {
                            "div_name": x["team"]["division"]["name"],
                            "teams": [],
                        }
                    }
                )

            team = {
                "name": x["team"]["name"],
                "div_rank": x["divisionRank"],
                "w": x["wins"],
                "l": x["losses"],
                "gb": x["gamesBack"],
                "wc_rank": x.get("wildCardRank", "-"),
                "wc_gb": x.get("wildCardGamesBack", "-"),
                "wc_elim_num": x.get("wildCardEliminationNumber", "-"),
                "elim_num": x.get("eliminationNumber", "-"),
                "team_id": x["team"]["id"],
                "league_rank": x.get("leagueRank", "-"),
                "sport_rank": x.get("sportRank", "-"),
            }
            divisions[x["team"]["division"]["id"]]["teams"].append(team)

    return divisions


def roster(teamId, rosterType=None, season=datetime.now().year, date=None):
    """Get the roster for a given team."""
    if not rosterType:
        rosterType = "active"

    params = {"rosterType": rosterType, "season": season, "teamId": teamId}
    if date:
        params.update({"date": date})

    r = get("team_roster", params)

    roster = ""
    players = []
    for x in r["roster"]:
        players.append(
            [x["jerseyNumber"], x["position"]["abbreviation"], x["person"]["fullName"]]
        )

    for i in range(0, len(players)):
        roster += ("#{:<3} {:<3} {}\n").format(*players[i])

    return roster


def meta(type, fields=None):
    """Get available values from StatsAPI for use in other queries,
    or look up descriptions for values found in API results.

    For example, to get a list of leader categories to use when calling team_leaders():
    statsapi.meta('leagueLeaderTypes')
    """
    types = [
        "awards",
        "baseballStats",
        "eventTypes",
        "freeGameTypes",
        "gameStatus",
        "gameTypes",
        "hitTrajectories",
        "jobTypes",
        "languages",
        "leagueLeaderTypes",
        "logicalEvents",
        "metrics",
        "pitchCodes",
        "pitchTypes",
        "platforms",
        "positions",
        "reviewReasons",
        "rosterTypes",
        "runnerDetailTypes",
        "scheduleTypes",
        "scheduleEventTypes",
        "situationCodes",
        "sky",
        "standingsTypes",
        "statGroups",
        "statTypes",
        "violationTypes",
        "windDirection",
    ]
    if type not in types:
        raise ValueError("Invalid meta type. Available meta types: %s." % types)

    return get("meta", {"type": type})


def notes(endpoint):
    """Get notes for a given endpoint."""
    msg = ""
    if not endpoint:
        msg = "No endpoint specified."
    else:
        if not ENDPOINTS.get(endpoint):
            msg = "Invalid endpoint specified."
        else:
            msg += "Endpoint: " + endpoint + " \n"
            path_params = [k for k, v in ENDPOINTS[endpoint]["path_params"].items()]
            required_path_params = [
                k
                for k, v in ENDPOINTS[endpoint]["path_params"].items()
                if v["required"]
            ]
            if required_path_params == []:
                required_path_params = "None"

            query_params = ENDPOINTS[endpoint]["query_params"]
            required_query_params = ENDPOINTS[endpoint]["required_params"]
            if required_query_params == [[]]:
                required_query_params = "None"
            msg += "All path parameters: %s. \n" % path_params
            msg += (
                "Required path parameters (note: ver will be included by default): %s. \n"
                % required_path_params
            )
            msg += "All query parameters: %s. \n" % query_params
            msg += "Required query parameters: %s. \n" % required_query_params
            if "hydrate" in query_params:
                msg += "The hydrate function is supported by this endpoint. Call the endpoint with {'hydrate':'hydrations'} in the parameters to return a list of available hydrations. For example, statsapi.get('schedule',{'sportId':1,'hydrate':'hydrations','fields':'hydrations'})\n"
            if ENDPOINTS[endpoint].get("note"):
                msg += "Developer notes: %s" % ENDPOINTS[endpoint].get("note")

    return msg


def get(endpoint, params={}, force=False, *, request_kwargs={}):
    """Call MLB StatsAPI and return JSON data.

    This function is for advanced querying of the MLB StatsAPI,
    and is used by the functions in this library.
    """
    # Lookup endpoint from input parameter
    ep = ENDPOINTS.get(endpoint)
    if not ep:
        raise ValueError("Invalid endpoint (" + str(endpoint) + ").")

    url = ep["url"]
    logger.debug("URL: {}".format(url))

    path_params = {}
    query_params = {}

    # Parse parameters into path and query parameters, and discard invalid parameters
    for p, pv in params.items():
        if ep["path_params"].get(p):
            logger.debug("Found path param: {}".format(p))
            if ep["path_params"][p].get("type") == "bool":
                if str(pv).lower() == "false":
                    path_params.update({p: ep["path_params"][p].get("False", "")})
                elif str(pv).lower() == "true":
                    path_params.update({p: ep["path_params"][p].get("True", "")})
            else:
                path_params.update({p: str(pv)})
        elif p in ep["query_params"]:
            logger.debug("Found query param: {}".format(p))
            query_params.update({p: str(pv)})
        else:
            if force:
                logger.debug(
                    "Found invalid param, forcing into query parameters per force flag: {}".format(
                        p
                    )
                )
                query_params.update({p: str(pv)})
            else:
                logger.debug("Found invalid param, ignoring: {}".format(p))

    logger.debug("path_params: {}".format(path_params))
    logger.debug("query_params: {}".format(query_params))

    # Replace path parameters with their values
    for k, v in path_params.items():
        logger.debug("Replacing {%s}" % k)
        url = url.replace(
            "{" + k + "}",
            ("/" if ep["path_params"][k]["leading_slash"] else "")
            + v
            + ("/" if ep["path_params"][k]["trailing_slash"] else ""),
        )
        logger.debug("URL: {}".format(url))

    while url.find("{") != -1 and url.find("}") > url.find("{"):
        param = url[url.find("{") + 1 : url.find("}")]
        if ep.get("path_params", {}).get(param, {}).get("required"):
            if (
                ep["path_params"][param]["default"]
                and ep["path_params"][param]["default"] != ""
            ):
                logger.debug(
                    "Replacing {%s} with default: %s."
                    % (param, ep["path_params"][param]["default"])
                )
                url = url.replace(
                    "{" + param + "}",
                    ("/" if ep["path_params"][param]["leading_slash"] else "")
                    + ep["path_params"][param]["default"]
                    + ("/" if ep["path_params"][param]["trailing_slash"] else ""),
                )
            else:
                if force:
                    logger.warning(
                        "Missing required path parameter {%s}, proceeding anyway per force flag..."
                        % param
                    )
                else:
                    raise ValueError("Missing required path parameter {%s}" % param)
        else:
            logger.debug("Removing optional param {%s}" % param)
            url = url.replace("{" + param + "}", "")

        logger.debug("URL: {}".format(url))
    # Add query parameters to the URL
    if len(query_params) > 0:
        for k, v in query_params.items():
            logger.debug("Adding query parameter {}={}".format(k, v))
            sep = "?" if url.find("?") == -1 else "&"
            url += sep + k + "=" + v
            logger.debug("URL: {}".format(url))

    # Make sure required parameters are present
    satisfied = False
    missing_params = []
    for x in ep.get("required_params", []):
        if len(x) == 0:
            satisfied = True
        else:
            missing_params.extend([a for a in x if a not in query_params])
            if len(missing_params) == 0:
                satisfied = True
                break

    if not satisfied and not force:
        if ep.get("note"):
            note = "\n--Endpoint note: " + ep.get("note")
        else:
            note = ""

        raise ValueError(
            "Missing required parameter(s): "
            + ", ".join(missing_params)
            + ".\n--Required parameters for the "
            + endpoint
            + " endpoint: "
            + str(ep.get("required_params", []))
            + ". \n--Note: If there are multiple sets in the required parameter list, you can choose any of the sets."
            + note
        )

    if len(request_kwargs):
        logger.debug(
            "Including request_kwargs in requests.get call: {}".format(request_kwargs)
        )

    # Make the request
    r = requests.get(url, **request_kwargs)
    if r.status_code not in [200, 201]:
        r.raise_for_status()
    else:
        return r.json()

    return None



================================================
FILE: statsapi/endpoints.py
================================================
#!/usr/bin/env python

BASE_URL = "https://statsapi.mlb.com/api/"

ENDPOINTS = {
    "attendance": {
        "url": BASE_URL + "{ver}/attendance",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "teamId",
            "leagueId",
            "season",
            "date",
            "leagueListId",
            "gameType",
            "fields",
        ],
        "required_params": [["teamId"], ["leagueId"], ["leagueListid"]],
    },
    "awards": {
        "url": BASE_URL + "{ver}/awards{awardId}{recipients}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "awardId": {
                "type": "str",
                "default": None,
                "leading_slash": True,
                "trailing_slash": False,
                "required": False,
            },
            "recipients": {
                "type": "bool",
                "default": True,
                "True": "/recipients",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
        },
        "query_params": ["sportId", "leagueId", "season", "hydrate", "fields"],
        "required_params": [[]],
        "note": "Call awards endpoint with no parameters to return a list of awardIds.",
    },
    "conferences": {
        "url": BASE_URL + "{ver}/conferences",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["conferenceId", "season", "fields"],
        "required_params": [[]],
    },
    "divisions": {
        "url": BASE_URL + "{ver}/divisions",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["divisionId", "leagueId", "sportId", "season"],
        "required_params": [[]],
        "note": "Call divisions endpoint with no parameters to return a list of divisions.",
    },
    "draft": {
        "url": BASE_URL + "{ver}/draft{prospects}{year}{latest}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "prospects": {
                "type": "bool",
                "default": False,
                "True": "/prospects",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
            "year": {
                "type": "str",
                "default": "",
                "leading_slash": True,
                "trailing_slash": False,
                "required": False,
            },
            "latest": {
                "type": "bool",
                "default": False,
                "True": "/latest",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
        },
        "query_params": [
            "limit",
            "fields",
            "round",
            "name",
            "school",
            "state",
            "country",
            "position",
            "teamId",
            "playerId",
            "bisPlayerId",
        ],
        "required_params": [[]],
        "note": 'No query parameters are honored when "latest" endpoint is queried (year is still required). Prospects and Latest cannot be used together.',
    },
    "game": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/live",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1.1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "hydrate", "fields"],
        "required_params": [[]],
    },
    "game_diff": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/live/diffPatch",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1.1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["startTimecode", "endTimecode"],
        "required_params": [["startTimecode", "endTimecode"]],
    },
    "game_timestamps": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/live/timestamps",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1.1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [],
        "required_params": [[]],
    },
    "game_changes": {
        "url": BASE_URL + "{ver}/game/changes",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["updatedSince", "sportId", "gameType", "season", "fields"],
        "required_params": [["updatedSince"]],
    },
    "game_contextMetrics": {
        "url": BASE_URL + "{ver}/game/{gamePk}/contextMetrics",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_winProbability": {
        "url": BASE_URL + "{ver}/game/{gamePk}/winProbability",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
        "note": "If you only want the current win probability for each team, try the game_contextMetrics endpoint instad.",
    },
    "game_boxscore": {
        "url": BASE_URL + "{ver}/game/{gamePk}/boxscore",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_content": {
        "url": BASE_URL + "{ver}/game/{gamePk}/content",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["highlightLimit"],
        "required_params": [[]],
    },
    "game_color": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/color",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_color_diff": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/color/diffPatch",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["startTimecode", "endTimecode"],
        "required_params": [["startTimeCode", "endTimeCode"]],
    },
    "game_color_timestamps": {
        "url": BASE_URL + "{ver}/game/{gamePk}/feed/color/timestamps",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [],
        "required_params": [[]],
    },
    "game_linescore": {
        "url": BASE_URL + "{ver}/game/{gamePk}/linescore",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_playByPlay": {
        "url": BASE_URL + "{ver}/game/{gamePk}/playByPlay",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "game_uniforms": {
        "url": BASE_URL + "{ver}/uniforms/game",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "gamePks",
            "fields",
        ],
        "required_params": [
            ["gamePks"],
        ],
    },
    "gamePace": {
        "url": BASE_URL + "{ver}/gamePace",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "season",
            "teamIds",
            "leagueIds",
            "leagueListId",
            "sportId",
            "gameType",
            "startDate",
            "endDate",
            "venueIds",
            "orgType",
            "includeChildren",
            "fields",
        ],
        "required_params": [["season"]],
    },
    "highLow": {
        "url": BASE_URL + "{ver}/highLow/{orgType}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "orgType": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [
            "statGroup",
            "sortStat",
            "season",
            "gameType",
            "teamId",
            "leagueId",
            "sportIds",
            "limit",
            "fields",
        ],
        "required_params": [["sortStat", "season"]],
        "note": "Valid values for orgType parameter: player, team, division, league, sport, types.",
    },
    "homeRunDerby": {
        "url": BASE_URL + "{ver}/homeRunDerby/{gamePk}{bracket}{pool}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "bracket": {
                "type": "bool",
                "default": False,
                "True": "/bracket",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
            "pool": {
                "type": "bool",
                "default": False,
                "True": "/pool",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
        },
        "query_params": ["fields"],
        "required_params": [[]],
    },
    "league": {
        "url": BASE_URL + "{ver}/league",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["sportId", "leagueIds", "seasons", "fields"],
        "required_params": [["sportId"], ["leagueIds"]],
    },
    "league_allStarBallot": {
        "url": BASE_URL + "{ver}/league/{leagueId}/allStarBallot",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "leagueId": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "fields"],
        "required_params": [["season"]],
    },
    "league_allStarWriteIns": {
        "url": BASE_URL + "{ver}/league/{leagueId}/allStarWriteIns",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "leagueId": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "fields"],
        "required_params": [["season"]],
    },
    "league_allStarFinalVote": {
        "url": BASE_URL + "{ver}/league/{leagueId}/allStarFinalVote",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "leagueId": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "fields"],
        "required_params": [["season"]],
    },
    "people": {
        "url": BASE_URL + "{ver}/people",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["personIds", "hydrate", "fields"],
        "required_params": [["personIds"]],
    },
    "people_changes": {
        "url": BASE_URL + "{ver}/people/changes",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["updatedSince", "fields"],
        "required_params": [[]],
    },
    "people_freeAgents": {
        "url": BASE_URL + "{ver}/people/freeAgents",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "leagueId": {
                "type": "str",
                "default": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["order", "hydrate", "fields"],
        "required_params": [[]],
    },
    "person": {
        "url": BASE_URL + "{ver}/people/{personId}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "personId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["hydrate", "fields"],
        "required_params": [[]],
    },
    "person_stats": {
        "url": BASE_URL + "{ver}/people/{personId}/stats/game/{gamePk}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "personId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "gamePk": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["fields"],
        "required_params": [[]],
        "note": 'Specify "current" instead of a gamePk for a player\'s current game stats.',
    },
    "jobs": {
        "url": BASE_URL + "{ver}/jobs",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["jobType", "sportId", "date", "fields"],
        "required_params": [["jobType"]],
    },
    "jobs_umpires": {
        "url": BASE_URL + "{ver}/jobs/umpires",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["sportId", "date", "fields"],
        "required_params": [[]],
    },
    "jobs_umpire_games": {
        "url": BASE_URL + "{ver}/jobs/umpires/games/{umpireId}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "umpireId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "fields"],
        "required_params": [["season"]],
    },
    "jobs_datacasters": {
        "url": BASE_URL + "{ver}/jobs/datacasters",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["sportId", "date", "fields"],
        "required_params": [[]],
    },
    "jobs_officialScorers": {
        "url": BASE_URL + "{ver}/jobs/officialScorers",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["timecode", "fields"],
        "required_params": [[]],
    },
    "schedule": {
        "url": BASE_URL + "{ver}/schedule",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "scheduleType",
            "eventTypes",
            "hydrate",
            "teamId",
            "leagueId",
            "sportId",
            "gamePk",
            "gamePks",
            "venueIds",
            "gameTypes",
            "date",
            "startDate",
            "endDate",
            "opponentId",
            "fields",
            "season",
        ],
        "required_params": [["sportId"], ["gamePk"], ["gamePks"]],
    },
    "schedule_tied": {
        "url": BASE_URL + "{ver}/schedule/games/tied",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["gameTypes", "season", "hydrate", "fields"],
        "required_params": [["season"]],
    },
    "schedule_postseason": {
        "url": BASE_URL + "{ver}/schedule/postseason",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "gameTypes",
            "seriesNumber",
            "teamId",
            "sportId",
            "season",
            "hydrate",
            "fields",
        ],
        "required_params": [[]],
    },
    "schedule_postseason_series": {
        "url": BASE_URL + "{ver}/schedule/postseason/series",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "gameTypes",
            "seriesNumber",
            "teamId",
            "sportId",
            "season",
            "fields",
        ],
        "required_params": [[]],
    },
    "schedule_postseason_tuneIn": {
        "url": BASE_URL + "{ver}/schedule/postseason/tuneIn",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["teamId", "sportId", "season", "hydrate", "fields"],
        "required_params": [[]],
        "note": "The schedule_postseason_tuneIn endpoint appears to return no data.",
    },
    "seasons": {
        "url": BASE_URL + "{ver}/seasons{all}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "all": {
                "type": "bool",
                "default": False,
                "True": "/all",
                "False": "",
                "leading_slash": False,
                "trailing_slash": False,
                "required": False,
            },
        },
        "query_params": ["season", "sportId", "divisionId", "leagueId", "fields"],
        "required_params": [["sportId"], ["divisionId"], ["leagueId"]],
        "note": 'Include "all" parameter with value of True to query all seasons. The divisionId and leagueId parameters are supported when "all" is used.',
    },
    "season": {
        "url": BASE_URL + "{ver}/seasons/{seasonId}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "seasonId": {
                "type": "str",
                "default": False,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["sportId", "fields"],
        "required_params": [["sportId"]],
    },
    "sports": {
        "url": BASE_URL + "{ver}/sports",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["sportId", "fields"],
        "required_params": [[]],
    },
    "sports_players": {
        "url": BASE_URL + "{ver}/sports/{sportId}/players",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "sportId": {
                "type": "str",
                "default": "1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "gameType", "fields"],
        "required_params": [["season"]],
    },
    "standings": {
        "url": BASE_URL + "{ver}/standings",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "leagueId",
            "season",
            "standingsTypes",
            "date",
            "hydrate",
            "fields",
        ],
        "required_params": [["leagueId"]],
    },
    "stats": {
        "url": BASE_URL + "{ver}/stats",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "stats",
            "playerPool",
            "position",
            "teamId",
            "leagueId",
            "limit",
            "offset",
            "group",
            "gameType",
            "season",
            "sportIds",
            "sortStat",
            "order",
            "hydrate",
            "fields",
            "personId",
            "metrics",
            "startDate",
            "endDate",
        ],
        "required_params": [["stats", "group"]],
        "note": "If no limit is specified, the response will be limited to 50 records.",
    },
    "stats_leaders": {
        "url": BASE_URL + "{ver}/stats/leaders",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "leaderCategories",
            "playerPool",
            "leaderGameTypes",
            "statGroup",
            "season",
            "leagueId",
            "sportId",
            "hydrate",
            "limit",
            "fields",
            "statType",
        ],
        "required_params": [["leaderCategories"]],
        "note": "If excluding season parameter to get all time leaders, include statType=statsSingleSeason or you will likely not get any results.",
    },
    "stats_streaks": {
        "url": BASE_URL + "{ver}/stats/streaks",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "streakType",
            "streakSpan",
            "gameType",
            "season",
            "sportId",
            "limit",
            "hydrate",
            "fields",
        ],
        "required_params": [["streakType", "streakSpan", "season", "sportId", "limit"]],
        "note": 'Valid streakType values: "hittingStreakOverall" "hittingStreakHome" "hittingStreakAway" "onBaseOverall" "onBaseHome" "onBaseAway". Valid streakSpan values: "career" "season" "currentStreak" "currentStreakInSeason" "notable" "notableInSeason".',
    },
    "teams": {
        "url": BASE_URL + "{ver}/teams",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "season",
            "activeStatus",
            "leagueIds",
            "sportId",
            "sportIds",
            "gameType",
            "hydrate",
            "fields",
        ],
        "required_params": [[]],
    },
    "teams_history": {
        "url": BASE_URL + "{ver}/teams/history",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["teamIds", "startSeason", "endSeason", "fields"],
        "required_params": [["teamIds"]],
    },
    "teams_stats": {
        "url": BASE_URL + "{ver}/teams/stats",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "season",
            "sportIds",
            "group",
            "gameType",
            "stats",
            "order",
            "sortStat",
            "fields",
            "startDate",
            "endDate",
        ],
        "required_params": [["season", "group", "stats"]],
        "note": "Use meta('statGroups') to look up valid values for group, and meta('statTypes') for valid values for stats.",
    },
    "teams_affiliates": {
        "url": BASE_URL + "{ver}/teams/affiliates",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["teamIds", "sportId", "season", "hydrate", "fields"],
        "required_params": [["teamIds"]],
    },
    "team": {
        "url": BASE_URL + "{ver}/teams/{teamId}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "sportId", "hydrate", "fields"],
        "required_params": [[]],
    },
    "team_alumni": {
        "url": BASE_URL + "{ver}/teams/{teamId}/alumni",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "group", "hydrate", "fields"],
        "required_params": [["season", "group"]],
    },
    "team_coaches": {
        "url": BASE_URL + "{ver}/teams/{teamId}/coaches",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["season", "date", "fields"],
        "required_params": [[]],
    },
    "team_personnel": {
        "url": BASE_URL + "{ver}/teams/{teamId}/personnel",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["date", "fields"],
        "required_params": [[]],
    },
    "team_leaders": {
        "url": BASE_URL + "{ver}/teams/{teamId}/leaders",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [
            "leaderCategories",
            "season",
            "leaderGameTypes",
            "hydrate",
            "limit",
            "fields",
        ],
        "required_params": [["leaderCategories", "season"]],
    },
    "team_roster": {
        "url": BASE_URL + "{ver}/teams/{teamId}/roster",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": ["rosterType", "season", "date", "hydrate", "fields"],
        "required_params": [[]],
    },
    "team_stats": {
        "url": BASE_URL + "{ver}/teams/{teamId}/stats",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "teamId": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [
            "season",
            "group",
            "gameType",
            "stats",
            "sportIds",
            "sitCodes",
            "fields",
        ],
        "required_params": [["season", "group"]],
        "note": "Use meta('statGroups') to look up valid values for group, meta('statTypes') for valid values for stats, and meta('situationCodes') for valid values for sitCodes. Use sitCodes with stats=statSplits.",
    },
    "team_uniforms": {
        "url": BASE_URL + "{ver}/uniforms/team",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "teamIds",
            "season",
            "fields",
        ],
        "required_params": [
            ["teamIds"],
        ],
    },
    "transactions": {
        "url": BASE_URL + "{ver}/transactions",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": [
            "teamId",
            "playerId",
            "date",
            "startDate",
            "endDate",
            "sportId",
            "fields",
        ],
        "required_params": [
            ["teamId"],
            ["playerId"],
            ["date"],
            ["startDate", "endDate"],
        ],
    },
    "venue": {
        "url": BASE_URL + "{ver}/venues",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            }
        },
        "query_params": ["venueIds", "season", "hydrate", "fields"],
        "required_params": [["venueIds"]],
    },
    "meta": {
        "url": BASE_URL + "{ver}/{type}",
        "path_params": {
            "ver": {
                "type": "str",
                "default": "v1",
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
            "type": {
                "type": "str",
                "default": None,
                "leading_slash": False,
                "trailing_slash": False,
                "required": True,
            },
        },
        "query_params": [[]],
        "required_params": [[]],
        "note": "The meta endpoint is used to retrieve values to be used within other API calls. Available types: awards, baseballStats, eventTypes, gameStatus, gameTypes, hitTrajectories, jobTypes, languages, leagueLeaderTypes, logicalEvents, metrics, pitchCodes, pitchTypes, platforms, positions, reviewReasons, rosterTypes, scheduleEventTypes, situationCodes, sky, standingsTypes, statGroups, statTypes, windDirection.",
    },
    # v1/analytics - requires authentication
    # v1/game/{gamePk}/guids - statcast data - requires authentication
}



================================================
FILE: statsapi/version.py
================================================
#!/usr/bin/env python

VERSION = "1.9.0"



================================================
FILE: tests/__init__.py
================================================



================================================
FILE: tests/test_get.py
================================================
import statsapi
import pytest
import requests.exceptions
import responses


def fake_dict():
    return {
        "foo": {
            "url": "http://www.foo.com",
            "path_params": {
                "ver": {
                    "type": "str",
                    "default": "v1",
                    "leading_slash": False,
                    "trailing_slash": False,
                    "required": True,
                }
            },
            "query_params": ["bar"],
            "required_params": [[]],
        }
    }


def test_get_returns_dictionary(mocker):
    # mock the ENDPOINTS dictionary
    mocker.patch.dict("statsapi.ENDPOINTS", fake_dict(), clear=True)
    # mock the requests object
    mock_req = mocker.patch("statsapi.requests", autospec=True)
    # mock the status code to always be 200
    mock_req.get.return_value.status_code = 200

    result = statsapi.get("foo", {"bar": "baz"})
    # assert that result is the same as the return value from calling the json method of a response object
    assert result == mock_req.get.return_value.json.return_value


def test_get_calls_correct_url(mocker):
    # mock the ENDPOINTS dictionary
    mocker.patch.dict("statsapi.ENDPOINTS", fake_dict(), clear=True)
    # mock the requests object
    mock_req = mocker.patch("statsapi.requests", autospec=True)

    statsapi.get("foo", {"bar": "baz"})
    mock_req.get.assert_called_with("http://www.foo.com?bar=baz")


@responses.activate
def test_get_server_error(mocker):
    # mock the ENDPOINTS dictionary
    mocker.patch.dict("statsapi.ENDPOINTS", fake_dict(), clear=True)
    responses.add(responses.GET, "http://www.foo.com?bar=baz", status=500)

    with pytest.raises(requests.exceptions.HTTPError):
        statsapi.get("foo", {"bar": "baz"})


def test_get_invalid_endpoint(mocker):
    # mock the ENDPOINTS dictionary
    mocker.patch.dict("statsapi.ENDPOINTS", fake_dict(), clear=True)
    # mock the requests object
    mock_req = mocker.patch("statsapi.requests", autospec=True)
    # invalid endpoint
    with pytest.raises(ValueError):
        statsapi.get("bar", {"foo": "baz"})

    # TODO: add test for path requirement not met
    # TODO: add test for required params



================================================
FILE: .github/FUNDING.yml
================================================
# These are supported funding model platforms

github: [toddrob99]
patreon: # Replace with a single Patreon username
open_collective: # Replace with a single Open Collective username
ko_fi: # Replace with a single Ko-fi username
tidelift: # Replace with a single Tidelift platform-name/package-name e.g., npm/babel
community_bridge: # Replace with a single Community Bridge project-name e.g., cloud-foundry
liberapay: # Replace with a single Liberapay username
issuehunt: # Replace with a single IssueHunt username
otechie: # Replace with a single Otechie username
custom: ['https://paypal.me/toddrob','https://cash.me/toddrob']



================================================
FILE: .github/workflows/release.yml
================================================
name: Build & Deploy to PyPI on Release

on:
  release:
    types: [released]

jobs:
    deploy:
      name: PyPI Deploy
      runs-on: ubuntu-latest
      steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - id: dist
        uses: casperdcl/deploy-pypi@v2
        with:
          requirements: twine setuptools wheel
          build: true
          password: ${{ secrets.PYPI_TOKEN }}
          upload: true


