/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/netanim-module.h"

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1
//    point-to-point
//

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("FirstScriptExample");

int
main(int argc, char* argv[])
{
    // set up the command line fr parsing
    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    // setting up time and its unit to nanoseconds
    // also setting up the level of logs
    Time::SetResolution(Time::NS);
    LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);

    // creating two nodes
    NodeContainer nodes;
    nodes.Create(2);

    // setting up the point to point data rate and delay
    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    // installing the devices in between the nodes
    NetDeviceContainer devices;
    devices = pointToPoint.Install(nodes);

    // setting up the internet stack in both the nodes fr IP communication
    InternetStackHelper stack;
    stack.Install(nodes);

    // setting the base IP address and subnet mask
    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");

    // assigning the IP address to each of the nodes
    Ipv4InterfaceContainer interfaces = address.Assign(devices);

    // setting up the UDP server helper at port 9
    UdpEchoServerHelper echoServer(9);

    // setting up the server at node 1, setting its time
    ApplicationContainer serverApps = echoServer.Install(nodes.Get(1));
    serverApps.Start(Seconds(1.0));
    serverApps.Stop(Seconds(10.0));

    // setting up client helper at port 9 and address at pos 1 and als its ther attributes
    UdpEchoClientHelper echoClient(interfaces.GetAddress(1), 9);
    echoClient.SetAttribute("MaxPackets", UintegerValue(1));
    echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
    echoClient.SetAttribute("PacketSize", UintegerValue(1024));

    // setting up the UDP client applicatin at node 0 and setting up its time
    ApplicationContainer clientApps = echoClient.Install(nodes.Get(0));
    clientApps.Start(Seconds(2.0));
    clientApps.Stop(Seconds(10.0));

    // Assignment 14 part1
    // setting up the animation by fixing the ndes at specific locations n the grid
    AnimationInterface anim("anim_p1.xml");
    anim.SetConstantPosition(nodes.Get(0),0.0,0.0);
    anim.SetConstantPosition(nodes.Get(1),150.0,150.0);

    // running and destrouying the simulator
    Simulator::Run();
    Simulator::Destroy();
    return 0;
}
